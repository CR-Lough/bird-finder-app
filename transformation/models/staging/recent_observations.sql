with final as (
    select
        species_code as 'species_code',
        com_name as 'com_name',
        sci_name as 'sci_name',
        loc_id as 'loc_id',
        loc_name as 'loc_name',
        obs_dt as 'obs_dt',
        how_many as 'how_many',
        lat as 'lat',
        lng as 'lng',
        obs_valid as 'obs_valid',
        obs_reviewed as 'obs_reviewed',
        location_private as 'location_private',
        sub_id as 'sub_id',
        subnational2_code as 'subnational2_code',
        subnational2_name as 'subnational2_name',
        subnational1_code as 'subnational1_code',
        subnational1_name as 'subnational1_name',
        country_code as 'country_code',
        country_name as 'country_name',
        user_display_name as 'user_display_name',
        obs_id as 'obs_id',
        checklist_id as 'checklist_id',
        presence_noted as 'presence_noted',
        has_comments as 'has_comments',
        first_name as 'first_name',
        last_name as 'last_name',
        has_rich_media as 'has_rich_media',
        _dlt_load_id as '_dlt_load_id',
        _dlt_id as '_dlt_id',
        evidence as 'evidence',
        exotic_category as 'exotic_category'
    from {{ source('ebirdapi', 'recent_observations') }}
)
select * from final