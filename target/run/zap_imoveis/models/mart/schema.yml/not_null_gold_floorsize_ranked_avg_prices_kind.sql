select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select kind
from "foo"."zap"."gold_floorsize_ranked_avg_prices"
where kind is null



      
    ) dbt_internal_test