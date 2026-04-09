import os
import pandas as pd
import random

os.makedirs('data', exist_ok=True)

# 1000 realistic Instagram-style usernames
real_usernames = [
    "apple","nike","google","mrbeast","elonmusk","tech_guru","foodie_life","fitness_king",
    "the_real_chef","travelgram_daily","sunset_vibes","photography_world","gym_motivation",
    "dev_codex","startup_hustle","crypto_moves","ai_insights","digital_nomad_life",
    "coffee_and_code","fashion_nova_daily","glow_up_journey","cutie_aesthetics",
    "urban_explorer","daily_grind_life","mindset_unlocked","chill_vibes_only",
    "business_blueprint","morning_routine_pro","healthyeats_daily","fitlife_journey",
    "skincare_secrets","plantbased_kitchen","yoga_everyday","running_madness",
    "vegan_recipes_daily","keto_life","workout_motivation","body_transformation",
    "aesthetic_feed","sunset_chaser","beach_therapy","wanderlust_diaries",
    "travel_with_me","globe_trekker","adventure_awaits","mountains_and_beyond",
    "hidden_gems_travel","solo_travel_life","backpacker_diaries","world_explorer_ig",
    "luxury_travel_mode","streets_of_the_world","food_therapy_daily","burger_obsessed",
    "pasta_dreams","sushi_lover_official","homecooking_hub","baking_with_love",
    "dessert_diaries","street_food_finds","restaurant_hopper","chef_life_daily",
    "spice_of_life_food","plant_kitchen_vibes","sneaker_culture","hype_kicks",
    "streetwear_daily","fashion_for_men","ootd_daily","style_inspiration",
    "minimalist_wardrobe","luxury_drip","vintage_finds","thrift_queen",
    "makeup_magic","beauty_insider","skincare_routine","glow_goals",
    "nail_art_daily","hair_transformation","glam_by_night","natural_beauty_tips",
    "crypto_daily","web3_explorer","blockchain_builder","nft_insider",
    "defi_digest","bitcoin_breakdowns","ethereum_explained","tech_startup_life",
    "founder_mode","vc_funded_journey","product_builder","side_hustle_empire",
    "passive_income_pro","personal_finance_101","invest_smarter","money_mindset",
    "stock_market_insider","real_estate_wins","freelance_life","remote_work_daily",
    "creative_agency","brand_builder","social_media_tips","content_creator_hub",
    "youtube_growth","podcast_daily","newsletter_king","email_marketing_pro",
    "seo_mastery","ads_performance","growth_hacking_101","community_builder",
    "mental_health_daily","self_care_rituals","therapy_in_practice","mindfulness_corner",
    "gratitude_daily","journaling_life","book_nerd_official","reading_habits",
    "fiction_addict","nonfiction_notes","learning_everyday","study_motivation",
    "university_life","campus_hustle","dorm_room_diaries","grad_school_grind",
    "science_explained","history_unboxed","philosophy_corner","economics_made_easy",
    "data_science_hub","machine_learning_daily","ai_art_gallery","prompt_engineering",
    "coding_bootcamp","web_dev_daily","react_mastery","python_tricks",
    "javascript_tips","fullstack_builder","devops_daily","cloud_architecture",
    "cybersecurity_now","open_source_life","github_explorer","terminal_life",
    "linux_tips","vim_master","keyboard_warrior","hardware_insider",
    "gaming_daily","esports_update","twitch_streamer_life","game_dev_journey",
    "retro_gaming_hub","console_wars","fps_gamer","rpg_adventures",
    "anime_universe","manga_shelf","cosplay_community","comic_collector",
    "movie_buff_daily","cinema_reviews","series_binge","netflix_picks",
    "music_producer_life","beatmaker_daily","vinyl_collector","indie_artist",
    "live_music_fan","concert_culture","guitar_life","piano_practice",
    "singer_songwriter","studio_sessions","dj_life_official","trap_music_hub",
    "jazz_vibes","classical_corner","podcast_recommendations","true_crime_fan",
    "documentary_lover","nature_photography","wildlife_captures","macro_lens_magic",
    "portrait_studio","street_photography","film_photography","drone_shots",
    "golden_hour_pics","composition_tips","light_and_shadow","analog_photography",
    "interior_design_daily","home_decor_ideas","minimalist_home","cozy_corners",
    "apartment_therapy","diy_everything","crafts_corner","pottery_life",
    "candle_making","plant_parenthood","succulents_obsessed","garden_therapy",
    "urban_farming","zero_waste_living","sustainable_lifestyle","eco_friendly_daily",
    "climate_action_now","green_planet","ocean_advocate","wildlife_conservation",
    "animal_lover_official","rescue_pets","dog_dad_life","cat_mom_hub",
    "pet_photography","horse_riding_life","bird_watching_daily","reef_aquarium",
    "fitness_coach_official","personal_trainer_hub","crossfit_culture","pilates_life",
    "boxing_gym_life","martial_arts_daily","swimming_journey","cycling_community",
    "trail_running_hub","soccer_fanatic","basketball_culture","tennis_life",
    "golf_swing_daily","volleyball_vibes","rugby_nation","cricket_updates",
    "formula1_fan","motorsport_hub","car_culture_daily","jdm_lifestyle",
    "american_muscle","electric_vehicle_hub","aviation_enthusiast","space_exploration",
    "astronomy_daily","physics_simplified","chemistry_lab","biology_explained",
    "math_made_fun","robotics_hub","3d_printing_life","maker_culture",
    "entrepreneurship_daily","ceo_mindset","leadership_lessons","team_building_tips",
    "productivity_hacks","deep_work_daily","time_management_pro","habits_that_stick",
    "atomic_habits_fan","stoic_philosophy","meditation_guide","breathwork_daily",
    "cold_plunge_life","biohacking_hub","longevity_research","sleep_science",
    "nutrition_decoded","gut_health_tips","hormones_explained","immune_boost",
    "intermittent_fasting","strength_training","hypertrophy_tips","mobility_work",
    "stretching_daily","posture_correction","pain_free_life","injury_prevention",
    "running_technique","marathon_training","triathlon_journey","spartan_race_life",
    "obstacle_course_training","calisthenics_daily","parkour_world","rock_climbing_hub",
    "surf_culture","snowboard_life","ski_trip_diaries","camping_adventures",
    "overlanding_life","van_life_diaries","tiny_house_movement","off_grid_living",
    "solar_powered_life","homesteading_hub","permaculture_farm","regenerative_ag",
    "beekeeping_life","mushroom_cultivation","fermentation_station","sourdough_life",
    "kombucha_culture","herbalism_daily","essential_oils_hub","natural_remedies",
    "ayurveda_life","traditional_medicine","eastern_wellness","holistic_health",
    "spirituality_daily","astrology_hub","tarot_readings","crystals_and_gems",
    "moon_rituals","manifestation_lab","law_of_attraction","energy_healing",
    "reiki_practice","chakra_alignment","sound_healing","shamanic_journey",
    "lucid_dreaming","quantum_mindset","consciousness_explored","sacred_geometry",
    "ancient_wisdom","mythology_hub","folklore_corner","cultural_heritage",
    "language_learning","polyglot_life","linguistics_corner","etymology_daily",
    "writing_craft","fiction_writing_tips","screenwriting_hub","poetry_collective",
    "spoken_word_artists","literary_criticism","creative_writing_daily","copywriting_pro",
    "ux_design_daily","product_design_hub","graphic_design_tips","typography_obsessed",
    "color_theory_lab","illustration_daily","motion_graphics","3d_art_world",
    "generative_art","nft_art_drops","pixel_art_hub","concept_art_daily",
    "architecture_daily","urban_planning","sustainable_design","biophilic_design",
    "parametric_design","landscape_architecture","interior_renders","real_estate_design",
    "civil_engineering","structural_engineering","mechanical_engineering","aerospace_hub",
    "naval_architecture","nuclear_science","quantum_computing","photonics_lab",
    "materials_science","nanotechnology","biotechnology_daily","genomics_hub",
    "crispr_explained","neuroscience_daily","cognitive_science","behavioral_economics",
    "positive_psychology","social_psychology","anthropology_corner","sociology_simplified",
    "political_science_hub","international_relations","global_news_digest","economics_daily",
    "market_analysis","geopolitics_explained","diplomacy_corner","human_rights_hub",
    "journalism_today","investigative_reporting","media_literacy","fact_check_daily",
    "data_journalism","infographic_design","visualization_hub","dashboards_pro",
    "excel_mastery","spreadsheet_wizard","automation_corner","rpa_life",
    "zapier_hacks","notion_templates","productivity_systems","second_brain_daily",
    "pkm_community","obsidian_daily","roam_research_hub","anki_for_learning",
    "spaced_repetition","ultralearning_hub","memory_palace","speed_reading",
    "critical_thinking","logic_puzzles","debate_club","rhetoric_mastery",
    "negotiation_skills","conflict_resolution","communication_pro","public_speaking",
    "storytelling_craft","presentation_design","video_production","cinematography_hub",
    "film_making_daily","editing_mastery","color_grading","vfx_breakdown",
    "sound_design","foley_artist","score_composition","music_theory_hub",
    "harmony_explained","music_production_101","ableton_tips","fl_studio_hub",
    "logic_pro_daily","vocal_training","singing_lessons","performance_coaching",
    "stage_presence","acting_daily","improv_comedy","stand_up_comedy",
    "sketch_comedy","variety_show_life","hosting_tips","emcee_culture",
    "brand_storytelling","content_strategy","seo_content","viral_content_lab",
    "short_form_video","reels_mastery","tiktok_strategy","youtube_shorts_hub",
    "influencer_journey","creator_economy","monetization_tips","brand_deals_101",
    "affiliate_marketing","dropshipping_life","ecommerce_tips","shopify_builder",
    "amazon_fba_hub","etsy_seller","handmade_business","small_biz_owner",
    "local_business_hub","franchise_life","restaurant_owner","retail_insider",
    "hospitality_biz","events_industry","wedding_planning","photography_biz",
    "freelance_design","consulting_life","coaching_business","online_courses_hub",
    "membership_site","community_platform","niche_newsletter","micro_saas",
    "product_led_growth","go_to_market","sales_strategy","revenue_operations",
    "customer_success","support_excellence","operations_daily","project_management",
    "agile_life","scrum_master","product_manager_hub","design_thinking",
    "innovation_lab","r_and_d_daily","patent_corner","ip_strategy",
    "legal_insights","startup_law","contracts_explained","equity_basics",
    "cap_table_101","fundraising_tips","pitch_deck_pro","investor_relations",
    "vc_world","angel_investing","accelerator_life","incubator_hub",
    "corporate_innovation","intrapreneurship","future_of_work","hr_insights",
    "talent_acquisition","employer_branding","people_ops","culture_builder",
    "diversity_inclusion","belonging_at_work","workplace_wellness",
]

# If we don't have enough, pad with themed ones
additional = [
    f"creator_{i:03d}" for i in range(1, 200)
] + [
    f"photo_art_{i:02d}" for i in range(1, 100)
] + [
    f"fit_coach_{i:02d}" for i in range(1, 100)
] + [
    f"chef_table_{i:02d}" for i in range(1, 100)
] + [
    f"tech_blog_{i:03d}" for i in range(1, 200)
]

all_usernames = real_usernames + additional
all_usernames = list(dict.fromkeys(all_usernames))[:1000]  # Deduplicate and cap at 1000

data = []
for u in all_usernames:
    followers = random.randint(500, 2500000)
    views = int(followers * random.uniform(0.5, 4.0))
    likes = int(views * random.uniform(0.05, 0.2))
    comments = int(views * random.uniform(0.01, 0.05))
    shares = int(views * random.uniform(0.02, 0.1))
    reposts = int(shares * random.uniform(0.1, 0.5))
    bio = "Official profile. Explore our latest updates and content."
    data.append([u, followers, views, likes, comments, shares, reposts, bio])

df = pd.DataFrame(data, columns=['username', 'followers', 'total_views', 'total_likes', 'total_comments', 'total_shares', 'total_reposts', 'bio'])
df.to_csv('data/instagram_db.csv', index=False)
print(f"Done! Generated {len(df)} accounts.")
print("Sample names:", list(df['username'].head(15)))
