
    
    

select
    id as unique_field,
    count(*) as n_records

from "foo"."zap"."gold_floorsize_ranked_avg_prices"
where id is not null
group by id
having count(*) > 1


