def build_prices_query(origin, destination, date_from, date_to,
                       can_be_nulled):

    if not can_be_nulled:
        price_identifier = 'avg(price)'
    else:
        price_identifier = 'case when count(*) > 3 then avg(price) end'
    # I used CTE for the conditions. I still find this faster than using the application layer
    # to determine the type of input and do multiple db requests.
    # The case here is we only have hundreds of ports globally (835 by count).
    # When benchmarking, the bottleneck will always be triggered by the prices table which
    # in reality will in millions.
    # So, adding some roundtrips through the application layer and doing multiple db requests
    # to check for the port codes will be more inefficient.
    return """with RECURSIVE orig_ports as (
            select distinct(a.code) as a_code from ports as a left join regions as b on a.parent_slug = b.slug  where b.slug = '{origin}'
            union all
            select distinct(a.code) as a_code from ports as a left join regions as b on a.parent_slug = b.slug  where b.parent_slug = '{origin}'
            union all
            select code from ports where code = '{origin}'
        ),
        dest_ports as (
            select distinct(a.code) as b_code from ports as a left join regions as b on a.parent_slug = b.slug  where b.slug = '{destination}'
            union all
            select distinct(a.code) as b_code from ports as a left join regions as b on a.parent_slug = b.slug  where b.parent_slug = '{destination}'
            union all
            select code from ports where code = '{destination}'
        ) SELECT day, {price_identifier}
            FROM prices
                inner join orig_ports on a_code = orig_code
                inner join dest_ports on b_code = dest_code
                where day >= '{date_from}' and day <= '{date_to}'
            group by day;""".format(
                origin=origin,
                destination=destination,
                date_from=date_from,
                date_to=date_to,
                price_identifier=price_identifier
        )
