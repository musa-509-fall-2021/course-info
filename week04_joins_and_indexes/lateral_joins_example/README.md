# A walkthrough of `lateral` joins

## Getting set up

To follow along with the code snippets in this walkthrough, download the following files:
* [credit_cards.csv](https://storage.googleapis.com/mjumbewu_musa_509/assn02_sample_data/credit_cards.csv)
* [purchases.csv](https://storage.googleapis.com/mjumbewu_musa_509/assn02_sample_data/purchases.csv)

In the _init_cc_tables.sql_ script, update the paths of the two files that you downloaded (right now they're set to full path of where the files were on my computer, but they need to point to where the files are on your computer). Copy the contents of the script and run in pgAdmin on your desired database (you may want to create a new database so that you can cleanly and easily destroy it later).

## Understanding the problem

**Our goal is to get the latest three purchase transactions (listed in the `credit_card_purchases` table) for each credit card (listed in the `credit_cards` table).** If there are fewer than three purchases for any credit card, then we just show all that there are. If there are no purchase for a credit card, we can just omit that card.

There are a few ways that we could do this, but PostgreSQL's `lateral` join feature provides the best option by far. The thing to understand is that in SQL it's generally easy to get some finite number of ordered records when we know what we're comparing against, but it's harder when we want to get some finite number of ordered records _with respect to some unknown number of other records_. For example, if we just wanted to get the 3 most recent transactions for the credit card number `4916261980884566`, that would be fairly simple:

_**Query 1** - 3 most recent purchases for CC number `4916261980884566`:_
```sql
select
    cc_number,
    purchase_id,
    purchase_amount,
    purchase_dt
from credit_card_purchases
where cc_number = '4916261980884566'
order by purchase_dt desc
limit 3
```

But if we want to repeat this for all of the `cc_number` values, we're out of luck. This is where `lateral` joins come in. The syntax for a later join is:

```sql
select t1.id, t2.id, ...
from first_table as t1
cross join lateral ( ... ) as t2
```

Whatever the query is that comes in the parentheses after `lateral` will be run for each row of the parent table (`first_table` in the example above). So, in our case, the parent table could be `credit_cards`, and we want our _**Query 1**_ to be run for each row of that table. So, the query that we would use is:

_**Query 2** - 3 most recent purchases for each CC number:_
```sql
select cc.cc_number, cc_pch.purchase_id, cc_pch.purchase_amount, cc_pch.purchase_dt
from credit_cards as cc
cross join lateral (
    select
        cc_number,
        purchase_id,
        purchase_amount,
        purchase_dt
    from credit_card_purchases as pch
    where pch.cc_number = cc.cc_number  -- <- That's the magic!
    order by purchase_dt desc
    limit 3
) as cc_pch;
```

The magic here is that a child query in a `lateral` join can reach outside of the parentheses to use values. Note that in the query above we're using a `cross join`. This is a common type of join with `lateral`, but is not necessary. If we want to include credit card numbers even when there are no related purchases, we can use a `left join` instead. If we do, we have to add a join condition (because only cross joins can be used without a join condition), but we can just make that condition `true` (try to puzzle out why we do that):

```sql
select cc.cc_number, cc_pch.purchase_id, cc_pch.purchase_amount, cc_pch.purchase_dt
from credit_cards as cc
left join lateral (
    select
        cc_number,
        purchase_id,
        purchase_amount,
        purchase_dt
    from credit_card_purchases as pch
    where pch.cc_number = cc.cc_number  -- <- That's the magic!
    order by purchase_dt desc
    limit 3
) as cc_pch
    on true;
```

## In summary...

Any time you have a task to get a finite number of ordered records from a table _`X`_ with respect to the records in some other table _`Y`_, if you're working in PostgreSQL you can take advantage of `lateral` joins. Think first about how you can retrieve the correct number of records from table _`X`_ given just one of the records of _Y_ (as in _**Query 1**_ above). Then take your query and wrap it in a parent query on table _`Y`_ (as in _**Query 2**_ above).
