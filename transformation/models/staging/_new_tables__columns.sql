with final as (
    select
        "name" as 'name',
        data_type as 'data_type',
        nullable as 'nullable',
        table_name as 'table_name',
        schema_name as 'schema_name',
        load_id as 'load_id',
        _dlt_parent_id as '_dlt_parent_id',
        _dlt_list_idx as '_dlt_list_idx',
        _dlt_id as '_dlt_id',
        "unique" as 'unique',
        foreign_key as 'foreign_key'
    from {{ source('ebirdapi', '_new_tables__columns') }}
)
select * from final