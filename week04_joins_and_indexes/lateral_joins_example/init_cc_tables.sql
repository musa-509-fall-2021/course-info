drop table if exists credit_cards;
create table credit_cards (
    cc_number text,
    cc_type text,
    cc_exp_date date
);

copy credit_cards
    from '/home/mjumbewu/Code/musa/musa-509/cross_joins_with_credit_cards/credit_cards.csv'
    with (format csv, header true);

drop table if exists credit_card_purchases;
create table credit_card_purchases (
    purchase_id integer,
    cc_number text,
    purchase_dt timestamp,
    purchase_amount decimal
);

copy credit_card_purchases
    from '/home/mjumbewu/Code/musa/musa-509/cross_joins_with_credit_cards/purchases.csv'
    with (format csv, header true);

drop index if exists credit_card_purchases__cc_number;
create index credit_card_purchases__cc_number
	on credit_card_purchases
	using btree (cc_number);
