select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select id
from "foo"."zap"."gold_floorsize_ranked_avg_prices"
where id is null



      
    ) dbt_internal_test