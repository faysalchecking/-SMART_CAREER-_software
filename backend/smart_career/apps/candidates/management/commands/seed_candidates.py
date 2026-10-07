from django.core.management.base import BaseCommand
from smart_career.apps.candidates.models import Candidate, Agent
import random

class Command(BaseCommand):
    help = 'Seed database with sample candidates'

    def handle(self, *args, **options):
        # Create sample agent
        agent, _ = Agent.objects.get_or_create(
            agent_id='AG-001',
            defaults={
                'company_name': 'Global Recruitment Solutions',
                'contact_person': 'Ahmed Hassan',
                'phone': '+880-1700-000000',
                'email': 'info@globalrecruit.com',
                'address': 'Dhaka, Bangladesh',
                'status': 'ACTIVE',
            }
        )

        candidates_data = [
            {
                'full_name': 'Mohammad Ali',
                'surname': 'Ali',
                'given_name': 'Mohammad',
                'date_of_birth': '1995-03-15',
                'gender': 'MALE',
                'nationality': 'Bangladesh',
                'mobile': '01700000001',
                'email': 'ali@example.com',
                'address': 'Dhaka, Bangladesh',
                'district': 'Dhaka',
                'upazila': 'Motijheel',
                'passport_number': 'PP0001',
                'passport_issue_date': '2020-05-10',
                'passport_expiry_date': '2030-05-10',
                'passport_issuing_country': 'Bangladesh',
                'education': 'Diploma in Electrical Engineering',
                'experience': '5 years as Electrician',
                'skills': 'Electrical Wiring, Panel Installation, Troubleshooting',
                'languages': 'Bengali, English',
                'preferred_country': 'Saudi Arabia',
                'preferred_position': 'Electrician',
                'current_status': 'AVAILABLE',
                'agent': agent,
            },
            {
                'full_name': 'Fatima Begum',
                'surname': 'Begum',
                'given_name': 'Fatima',
                'date_of_birth': '1998-07-22',
                'gender': 'FEMALE',
                'nationality': 'Bangladesh',
                'mobile': '01700000002',
                'email': 'fatima@example.com',
                'address': 'Chittagong, Bangladesh',
                'district': 'Chittagong',
                'upazila': 'Halishahar',
                'passport_number': 'PP0002',
                'passport_issue_date': '2021-08-15',
                'passport_expiry_date': '2031-08-15',
                'passport_issuing_country': 'Bangladesh',
                'education': 'Bachelor in Nursing',
                'experience': '3 years as Nurse',
                'skills': 'Patient Care, IV Administration, Monitoring',
                'languages': 'Bengali, English, Arabic',
                'preferred_country': 'UAE',
                'preferred_position': 'Nurse',
                'current_status': 'AVAILABLE',
                'agent': agent,
            },
            {
                'full_name': 'Hassan Rahman',
                'surname': 'Rahman',
                'given_name': 'Hassan',
                'date_of_birth': '1992-11-08',
                'gender': 'MALE',
                'nationality': 'Bangladesh',
                'mobile': '01700000003',
                'email': 'hassan@example.com',
                'address': 'Sylhet, Bangladesh',
                'district': 'Sylhet',
                'upazila': 'Sylhet',
                'passport_number': 'PP0003',
                'passport_issue_date': '2019-02-20',
                'passport_expiry_date': '2029-02-20',
                'passport_issuing_country': 'Bangladesh',
                'education': 'Vocational Training in Heavy Equipment',
                'experience': '7 years as Crane Operator',
                'skills': 'Crane Operation, Safety Management, Load Calculation',
                'languages': 'Bengali, English',
                'preferred_country': 'Qatar',
                'preferred_position': 'Crane Operator',
                'current_status': 'APPLIED',
                'agent': agent,
            },
            {
                'full_name': 'Aisha Khan',
                'surname': 'Khan',
                'given_name': 'Aisha',
                'date_of_birth': '1999-01-30',
                'gender': 'FEMALE',
                'nationality': 'Bangladesh',
                'mobile': '01700000004',
                'email': 'aisha@example.com',
                'address': 'Sylhet, Bangladesh',
                'district': 'Sylhet',
                'upazila': 'Sylhet',
                'passport_number': 'PP0004',
                'passport_issue_date': '2023-06-12',
                'passport_expiry_date': '2033-06-12',
                'passport_issuing_country': 'Bangladesh',
                'education': 'Degree in Hotel Management',
                'experience': '2 years as Housekeeper',
                'skills': 'Cleaning, Organization, Customer Service',
                'languages': 'Bengali, English',
                'preferred_country': 'Malaysia',
                'preferred_position': 'Housekeeper',
                'current_status': 'AVAILABLE',
                'agent': agent,
            },
            {
                'full_name': 'Ahmed Ibrahim',
                'surname': 'Ibrahim',
                'given_name': 'Ahmed',
                'date_of_birth': '1990-09-14',
                'gender': 'MALE',
                'nationality': 'Bangladesh',
                'mobile': '01700000005',
                'email': 'ahmed@example.com',
                'address': 'Khulna, Bangladesh',
                'district': 'Khulna',
                'upazila': 'Khulna City',
                'passport_number': 'PP0005',
                'passport_issue_date': '2018-12-10',
                'passport_expiry_date': '2028-12-10',
                'passport_issuing_country': 'Bangladesh',
                'education': 'Diploma in Mechanical Engineering',
                'experience': '8 years as Technician',
                'skills': 'Machine Maintenance, Repair, Installation',
                'languages': 'Bengali, English, Hindi',
                'preferred_country': 'Saudi Arabia',
                'preferred_position': 'Technician',
                'current_status': 'SHORTLISTED',
                'agent': agent,
            },
        ]

        created_count = 0
        for idx, data in enumerate(candidates_data, 1):
            # Generate simple candidate_id (SC-00001, SC-00002, etc)
            data['candidate_id'] = f"SC-{idx:05d}"

            candidate, created = Candidate.objects.get_or_create(
                mobile=data['mobile'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created: {candidate.full_name} ({candidate.candidate_id})")

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} candidates')
        )