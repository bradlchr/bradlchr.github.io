import os
import sys
import unittest
import json
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import get_db_connection, init_db, parse_json_fields
from app.auth import seed_default_users, hash_password, verify_password, generate_token, verify_token
from app.api import (
    handle_login, handle_demo_switch, get_plants_list,
    get_single_plant, create_plant, update_plant, delete_plant,
    export_report_markdown, get_stats
)

class DeepRootsTestSuite(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_default_users()

    def test_01_auth_system(self):
        # 1. Login with correct admin
        status, res = handle_login({'email': 'admin@deeproots.org', 'password': 'admin123'})
        self.assertEqual(status, 200)
        self.assertIn('token', res)
        self.assertEqual(res['user']['role'], 'admin')

        # 2. Login with correct advisor
        status, res = handle_login({'email': 'advisor@deeproots.org', 'password': 'advisor123'})
        self.assertEqual(status, 200)
        self.assertEqual(res['user']['role'], 'advisor')

        # 3. Invalid credentials
        status, res = handle_login({'email': 'advisor@deeproots.org', 'password': 'wrongpassword'})
        self.assertEqual(status, 401)

        # 4. Token verification
        admin_token = generate_token({'id': 'test-id', 'email': 'admin@deeproots.org', 'name': 'Admin', 'role': 'admin'})
        payload = verify_token(admin_token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload['email'], 'admin@deeproots.org')

    def test_02_database_and_facets(self):
        # Fetch all plants
        status, res = get_plants_list({})
        self.assertEqual(status, 200)
        self.assertGreaterEqual(res['total'], 180)
        self.assertIn('facets', res)
        
        # Verify facet counters exist
        facets = res['facets']
        self.assertIn('environment', facets)
        self.assertIn('Prairie', facets['environment'])
        self.assertGreater(facets['environment']['Prairie'], 0)
        self.assertIn('Forest', facets['environment'])
        self.assertGreater(facets['environment']['Forest'], 0)
        self.assertIn('light', facets)
        self.assertIn('Full Sun', facets['light'])
        self.assertIn('plant_type', facets)
        self.assertIn('Wildflower', facets['plant_type'])

    def test_03_search_and_filtering(self):
        # Search by query
        status, res = get_plants_list({'q': ['Serviceberry']})
        self.assertEqual(status, 200)
        self.assertGreaterEqual(res['total'], 2)
        sci_names = [p['scientific_name'] for p in res['plants']]
        self.assertTrue(any('Amelanchier' in s for s in sci_names))

        # Filter by environment and light
        status, res = get_plants_list({
            'environment': ['Prairie'],
            'light': ['Full Sun']
        })
        self.assertEqual(status, 200)
        for p in res['plants']:
            self.assertEqual(p['native_environment'], 'Prairie')
            self.assertIn('Full Sun', p['light_requirements'])

        # Filter by Deep Roots Sweet 16
        status, res = get_plants_list({'special_tags': ['Deep Roots Sweet 16']})
        self.assertEqual(status, 200)
        self.assertEqual(res['total'], 16)

    def test_04_plant_crud_and_rbac(self):
        admin_user = {'id': 'user-admin-01', 'email': 'admin@deeproots.org', 'role': 'admin'}
        advisor_user = {'id': 'user-advisor-01', 'email': 'advisor@deeproots.org', 'role': 'advisor'}

        test_sci = f"Testus botanicus {uuid.uuid4().hex[:6]}"
        new_plant_data = {
            'scientific_name': test_sci,
            'common_names': ['Botanical Test Plant'],
            'native_environment': 'Prairie',
            'plant_type': ['Wildflower'],
            'architectural_layer': 'Seasonal/Herbaceous Layer',
            'mature_height_min': 2.0,
            'mature_height_max': 4.0,
            'height_display': '2–4 ft',
            'bloom_color': ['Purple'],
            'bloom_period': ['July', 'August', 'Summer'],
            'soil_requirements': ['Loam', 'Clay'],
            'moisture_requirements': ['Medium'],
            'light_requirements': ['Full Sun'],
            'wildlife_ecosystem_benefits': ['Specialist Bees', 'Larval Host'],
            'sociability': 'Medium / Moderate Spreading',
            'advisor_description': 'An outstanding prairie specimen that delivers vibrant blooms and supports native bees.',
            'special_tags': ['KC Keystone'],
            'images': [{
                'url': 'https://example.com/test.jpg',
                'caption': 'In bloom',
                'attribution_name': 'Nature Photographer',
                'attribution_url': 'https://example.com',
                'license': 'CC BY-SA 4.0'
            }],
            'sources': [{
                'source_name': 'Missouri Botanical Garden',
                'source_url': 'https://missouribotanicalgarden.org',
                'notes': 'Test citation'
            }]
        }

        # 1. Advisor should be rejected from creating
        status, res = create_plant(new_plant_data, advisor_user)
        self.assertEqual(status, 403)

        # 2. Admin should succeed
        status, res = create_plant(new_plant_data, admin_user)
        self.assertEqual(status, 201)
        created_id = res['id']

        # 3. Retrieve single plant
        status, single = get_single_plant(created_id)
        self.assertEqual(status, 200)
        self.assertEqual(single['scientific_name'], test_sci)
        self.assertEqual(single['sociability'], 'Medium / Moderate Spreading')

        # 4. Update plant
        new_plant_data['advisor_description'] = 'Updated description with 3 lines or less for client consultations.'
        status, res = update_plant(created_id, new_plant_data, admin_user)
        self.assertEqual(status, 200)

        # 5. Delete plant as advisor -> 403
        status, res = delete_plant(created_id, advisor_user)
        self.assertEqual(status, 403)

        # 6. Delete plant as admin -> 200
        status, res = delete_plant(created_id, admin_user)
        self.assertEqual(status, 200)

        # Verify deletion
        status, res = get_single_plant(created_id)
        self.assertEqual(status, 404)

    def test_05_report_export(self):
        sample_report = {
            'client_name': 'Jane Doe',
            'project_name': 'Prairie Meadow & Shade Garden',
            'consultation_date': 'October 2026',
            'advisor_name': 'Cydney Ross',
            'summary_notes': 'Sunny front yard transformation replacing turf with a biodiverse native pollinator matrix.',
            'plants': [
                {
                    'scientific_name': 'Echinacea purpurea',
                    'common_names': ['Purple Coneflower'],
                    'native_environment': 'Prairie',
                    'architectural_layer': 'Seasonal/Herbaceous Layer',
                    'height_display': '2–4 ft',
                    'light_requirements': ['Full Sun', 'Part Sun'],
                    'moisture_requirements': ['Medium', 'Dry'],
                    'sociability': 'Medium / Moderate Spreading',
                    'advisor_description': 'Staple of native landscapes with wide appeal for hundreds of pollinators. Goldfinches feast on the seed cones in fall.',
                    'advisor_notes': 'Mass in clusters of 3-5 in the center border along the driveway.',
                    'special_tags': ['Deep Roots Sweet 16', 'KC Keystone']
                }
            ]
        }

        status, res = export_report_markdown(sample_report)
        self.assertEqual(status, 200)
        self.assertIn('markdown', res)
        md = res['markdown']
        self.assertIn('Deep Roots KC — Nature Advisor Consultation Report', md)
        self.assertIn('Echinacea purpurea', md)
        self.assertIn('Deep Roots Sweet 16', md)
        self.assertIn('Advisor Recommendations for Your Yard', md)

if __name__ == '__main__':
    unittest.main()
