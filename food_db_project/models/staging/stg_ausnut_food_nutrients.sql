with 
source as (
    select * from {{ source('raw','food_nutrient_profiles') }}
), 

renamed as (
    select 
        "Survey ID" as survey_id,
        "Food name" as food_name,
        "Energy without dietary fibre (kJ)" as energy_without_dietary_fibre_kj,
        "Protein (g)" as protein_g,
        "Total fat (g)" as total_fat_g,
        "Available carbohydrate, without sugar alcohols (g)" as available_carbohydrate_g_without_sugar_alcohols,
        "Total sugars (g)" as total_sugar_g,
        "Dietary fibre (g)" as total_dietary_fibre_g,
        "Iron (Fe) (mg)" as iron_fe_mg,
        "Calcium (Ca) (mg)" as calcium_ca_mg
    from source
)
select * from renamed


