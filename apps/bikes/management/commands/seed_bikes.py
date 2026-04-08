"""
Management command to seed the database with sample bike data.
"""

from django.core.management.base import BaseCommand
from apps.bikes.models import BikeCategory, Bike


class Command(BaseCommand):
    help = 'Seed the database with sample bike categories and bikes'

    def handle(self, *args, **options):
        self.stdout.write('🚴 Seeding Astral Sport database...\n')

        # Create categories
        categories_data = [
            {'name': 'Road Bike', 'slug': 'road-bike', 'description': 'Sepeda jalan raya untuk kecepatan tinggi', 'icon': '🏎️'},
            {'name': 'Mountain Bike', 'slug': 'mountain-bike', 'description': 'Sepeda gunung untuk medan off-road', 'icon': '🏔️'},
            {'name': 'Gravel Bike', 'slug': 'gravel-bike', 'description': 'Sepeda serbaguna untuk aspal dan tanah', 'icon': '🌄'},
            {'name': 'City Bike', 'slug': 'city-bike', 'description': 'Sepeda kota yang nyaman untuk harian', 'icon': '🏙️'},
            {'name': 'E-Bike', 'slug': 'e-bike', 'description': 'Sepeda listrik dengan motor assist', 'icon': '⚡'},
            {'name': 'Folding Bike', 'slug': 'folding-bike', 'description': 'Sepeda lipat untuk mobilitas urban', 'icon': '📦'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = BikeCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = cat
            status = '✅ Created' if created else '⏭️ Exists'
            self.stdout.write(f'  {status}: {cat.name}')

        # Create bikes
        bikes_data = [
            {
                'name': 'Viper Aero Pro',
                'slug': 'viper-aero-pro',
                'category': categories['road-bike'],
                'description': 'Sepeda road bike ultra-ringan dengan frame carbon fiber full monocoque. Dirancang untuk kecepatan maksimum di jalanan aspal. Aerodinamis dan responsif di setiap tikungan.',
                'tagline': 'Born to break speed limits',
                'price_per_hour': 50000,
                'price_per_day': 300000,
                'terrain_type': 'asphalt',
                'weight_kg': 8.2,
                'frame_material': 'Carbon Fiber',
                'gear_system': 'Shimano 105 R7000 22-Speed',
                'wheel_size': '700x25c',
                'total_units': 5,
                'available_units': 3,
                'calories_per_km': 32,
                'co2_saved_per_km': 210,
                'is_featured': True,
            },
            {
                'name': 'Titan XC Trail',
                'slug': 'titan-xc-trail',
                'category': categories['mountain-bike'],
                'description': 'Mountain bike tangguh dengan suspensi depan RockShox 120mm travel. Siap menaklukkan trail terberat. Frame aluminium alloy grade 6061 yang kokoh namun ringan.',
                'tagline': 'Conquer every trail',
                'price_per_hour': 45000,
                'price_per_day': 280000,
                'terrain_type': 'offroad',
                'weight_kg': 12.5,
                'frame_material': 'Aluminium Alloy 6061',
                'gear_system': 'Shimano Deore 12-Speed',
                'wheel_size': '29x2.25"',
                'total_units': 6,
                'available_units': 4,
                'calories_per_km': 45,
                'co2_saved_per_km': 210,
                'is_featured': True,
            },
            {
                'name': 'Nova Gravel X',
                'slug': 'nova-gravel-x',
                'category': categories['gravel-bike'],
                'description': 'Gravel bike serbaguna yang nyaman di aspal maupun jalan tanah. Frame chromoly steel memberikan kenyamanan ekstra pada perjalanan jauh. Best seller untuk weekend adventure.',
                'tagline': 'Where road meets adventure',
                'price_per_hour': 55000,
                'price_per_day': 320000,
                'terrain_type': 'mixed',
                'weight_kg': 9.8,
                'frame_material': 'Chromoly Steel',
                'gear_system': 'Shimano GRX 20-Speed',
                'wheel_size': '700x40c',
                'total_units': 4,
                'available_units': 2,
                'calories_per_km': 38,
                'co2_saved_per_km': 210,
                'is_featured': True,
            },
            {
                'name': 'Metro Cruiser',
                'slug': 'metro-cruiser',
                'category': categories['city-bike'],
                'description': 'City bike elegan untuk commuting harian. Dilengkapi fender penuh, lampu LED terintegrasi, dan carrier belakang. Posisi riding tegak yang nyaman untuk perjalanan santai.',
                'tagline': 'The urban companion',
                'price_per_hour': 35000,
                'price_per_day': 200000,
                'terrain_type': 'asphalt',
                'weight_kg': 14.0,
                'frame_material': 'Hi-Tensile Steel',
                'gear_system': 'Shimano Nexus 7-Speed Internal',
                'wheel_size': '700x35c',
                'total_units': 8,
                'available_units': 6,
                'calories_per_km': 28,
                'co2_saved_per_km': 210,
                'is_featured': True,
            },
            {
                'name': 'Volt E-Power',
                'slug': 'volt-e-power',
                'category': categories['e-bike'],
                'description': 'E-bike premium dengan motor Shimano Steps 250W dan baterai 504Wh. Jangkauan hingga 120km per charge. Cocok untuk pemula dan commuter yang ingin assist tenaga listrik.',
                'tagline': 'Effortless power on demand',
                'price_per_hour': 75000,
                'price_per_day': 450000,
                'terrain_type': 'mixed',
                'weight_kg': 22.0,
                'frame_material': 'Aluminium Alloy',
                'gear_system': 'Shimano Deore 10-Speed + Motor 250W',
                'wheel_size': '27.5x2.0"',
                'total_units': 3,
                'available_units': 2,
                'calories_per_km': 20,
                'co2_saved_per_km': 210,
                'is_featured': True,
            },
            {
                'name': 'Pact Fold Lite',
                'slug': 'pact-fold-lite',
                'category': categories['folding-bike'],
                'description': 'Sepeda lipat ultraportabel yang bisa dilipat dalam 10 detik. Frame aluminium ringan dengan mekanisme lipat quick-release. Ideal untuk commuter yang naik transportasi umum.',
                'tagline': 'Fold. Ride. Repeat.',
                'price_per_hour': 40000,
                'price_per_day': 240000,
                'terrain_type': 'asphalt',
                'weight_kg': 10.5,
                'frame_material': 'Aluminium Alloy',
                'gear_system': 'Shimano Tourney 7-Speed',
                'wheel_size': '20"',
                'total_units': 5,
                'available_units': 4,
                'calories_per_km': 30,
                'co2_saved_per_km': 210,
                'is_featured': True,
            },
            {
                'name': 'Aether TT',
                'slug': 'aether-tt',
                'category': categories['road-bike'],
                'description': 'Time trial road bike dengan geometri agresif dan aero bar terintegrasi. Carbon fiber full dengan routing kabel internal untuk aerodinamika maksimal.',
                'tagline': 'Slice through the wind',
                'price_per_hour': 65000,
                'price_per_day': 380000,
                'terrain_type': 'asphalt',
                'weight_kg': 7.8,
                'frame_material': 'Carbon Fiber T800',
                'gear_system': 'Shimano Ultegra Di2 22-Speed',
                'wheel_size': '700x23c',
                'total_units': 2,
                'available_units': 1,
                'calories_per_km': 35,
                'co2_saved_per_km': 210,
                'is_featured': False,
            },
            {
                'name': 'Ridge DH Pro',
                'slug': 'ridge-dh-pro',
                'category': categories['mountain-bike'],
                'description': 'Downhill mountain bike full suspension dengan travel 200mm depan dan belakang. Frame aluminium alloy yang tahan banting untuk terrain ekstrem.',
                'tagline': 'Gravity is your playground',
                'price_per_hour': 60000,
                'price_per_day': 350000,
                'terrain_type': 'offroad',
                'weight_kg': 16.5,
                'frame_material': 'Aluminium Alloy 7005',
                'gear_system': 'SRAM GX Eagle 12-Speed',
                'wheel_size': '27.5x2.5"',
                'total_units': 3,
                'available_units': 2,
                'calories_per_km': 50,
                'co2_saved_per_km': 210,
                'is_featured': False,
            },
        ]

        for bike_data in bikes_data:
            bike, created = Bike.objects.get_or_create(
                slug=bike_data['slug'],
                defaults=bike_data
            )
            status = '✅ Created' if created else '⏭️ Exists'
            self.stdout.write(f'  {status}: {bike.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Done! {BikeCategory.objects.count()} categories, {Bike.objects.count()} bikes in database.'
        ))
