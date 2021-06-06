create table personal_account 
(
	id varchar(3),
    name varchar(10),
    family_name varchar(10),
    type_of_account varchar(10) check (type_of_account in ('normal', 'prof', 'student', 'boss', 'reception')),
    primary key (id)
);

create table systematic_account
(
	id varchar(3),
    user_name varchar(30),
    password varchar(30),
    created_date varchar(10),
    account_balance numeric(5,0),
    warning numeric(3,0) default 0,
    primary key (user_name),
    foreign key (id) references personal_account(id)
);

create table user_address
(
	id varchar(3),
    address varchar(100),
    primary key (id, address),
    foreign key (id) references personal_account(id)
);

create table user_phone
(
	id varchar(3),
    phone_num varchar(100),
    primary key (id, phone_num),
    foreign key (id) references personal_account(id)
);


create table book
(
	book_id varchar(5),
    title varchar(10),
    category varchar(10),
    author varchar(10),
    edition varchar(3),
    price numeric(5,0),
    primary key (book_id)
);

create table history 
(
	id varchar(3),
    history_id MEDIUMINT NOT NULL AUTO_INCREMENT,
    book_id varchar(5),
    result varchar(30),
    start_date varchar(30) default null,
    returned_date varchar(30) default null,
    primary key (history_id),
    foreign key (id) references personal_account(id),
    foreign key (book_id) references book(book_id)
);

create table inventory 
(
	book_id varchar(5),
    quantity numeric(3,0) default 1,
    available_date numeric(3,0),
    primary key (book_id),
    foreign key (book_id) references book(book_id)
);



DELIMITER $$
START TRANSACTION;
create procedure insertIntoPersonal(IN id varchar(3), IN name varchar(10),IN family_name varchar(10), IN type_of_account Varchar(10))
    DETERMINISTIC
	begin
		insert into personal_account(id, name, family_name, type_of_account) values (id, name, family_name, type_of_account);
	end$$
COMMIT;
DELIMITER ;


create table inbox
(
	inbox_id MEDIUMINT NOT NULL AUTO_INCREMENT,
    message varchar(200),
    primary key (inbox_id)
);


DELIMITER $$
START TRANSACTION;
create procedure insertIntoSystematic(IN id varchar(3),IN user_name varchar(30),IN password varchar(30),IN account_balance numeric(5,0))
    DETERMINISTIC
	begin
		insert into systematic_account(id,user_name,password,created_date,account_balance) values (id,user_name,password,CURDATE(),account_balance);
	end$$
COMMIT;
DELIMITER ;


DELIMITER $$
create procedure insertIntoPhone(IN id varchar(3),IN phone_num varchar(100))
    DETERMINISTIC
	begin
		insert into user_phone(id, phone_num) values (id,phone_num);
	end$$
DELIMITER ;


DELIMITER $$
create procedure insertIntoAddress(IN id varchar(3),IN address varchar(100))
    DETERMINISTIC
	begin
		insert into user_address(id, address) values (id,address);
	end$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE CheckUserExists( IN usr varchar(30), IN pswd varchar(30))
BEGIN
      IF EXISTS(SELECT user_name, password
                        FROM systematic_account
                        WHERE user_name = usr and password = pswd)
      THEN 
            SET @val = 1;
      ELSE
            SET @val = 0;
      END IF;
	  select @val;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE getField(IN usr varchar(30))
BEGIN
	  select type_of_account
      from systematic_account natural join personal_account
      where usr = user_name;
END$$
DELIMITER ;


DELIMITER $$
create procedure InfoRetrieve(IN usr varchar(30))
begin
	select *
    from systematic_account natural join personal_account
    where usr = user_name;
end$$
DELIMITER ; 


DELIMITER $$
create procedure insertIntoBook(IN book_id varchar(5),IN title varchar(10),IN category varchar(10),IN author varchar(10),IN edition varchar(3),IN price numeric(5,0))
    DETERMINISTIC
	begin
		if checkBookExistance2(book_id) = 0 then
			insert into book(book_id, title, category, author, edition, price) values (book_id, title, category, author, edition, price)  ;
            select "Book Added!";
		else
			select "This book already exists! ";
		end if;
	end$$
DELIMITER ;


DELIMITER $$
create procedure insertIntoInventory(IN book_id varchar(5),IN avail_date numeric(3,0))
    DETERMINISTIC
	begin
		if checkBookExistance2(book_id) = 1 then
			insert into inventory(book_id, available_date) values (book_id, avail_date);
            select "Book Added!";
		else 
			select "this book doesn't exist! make one first";
		end if;
	end$$
DELIMITER ;



DELIMITER $$
create procedure updateInventory(IN bid varchar(5), IN num numeric(3,0))
    DETERMINISTIC
	begin
		IF EXISTS(SELECT book_id
                        FROM inventory
                        WHERE book_id = bid)
      THEN 
			update inventory 
            set quantity = quantity + num
            where book_id = bid;
            select "Book quantity increased";
      ELSE
            select "This book doesn't exist";
      END IF;
	end$$
DELIMITER ;


DELIMITER $$
create procedure updateUserCash(IN usr varchar(30), IN num numeric(5,0))
    DETERMINISTIC
	begin
		IF num > (SELECT 0) 
      THEN 
			update systematic_account 
            set account_balance = account_balance + num
            where user_name = usr;
            SET @val = 'balance increased';
      ELSE
            SET @val = 'You entered wrong amount';
      END IF;
	  select @val;
	end$$
DELIMITER ;



DELIMITER $$
create procedure userSearch1(IN Pname varchar(10))
    DETERMINISTIC
	begin
		select *
        from personal_account
        where pname = name;
	end$$
DELIMITER ;


DELIMITER $$
create procedure userSearch2(IN fname varchar(10))
    DETERMINISTIC
	begin
		select *
        from personal_account
        where fname = family_name;
	end$$
DELIMITER ;


DELIMITER $$
create function checkBookExistance2(bid varchar(5))
returns integer deterministic
begin
declare result integer;
	IF EXISTS(SELECT book_id
                        FROM book
                        WHERE book_id = bid)
      THEN 
            SET result = 1;
      ELSE
            SET result = 0;
      END IF;
      return result;
end$$
DELIMITER ;

DELIMITER $$
create function checkBookExistance(bid varchar(5))
returns integer deterministic
begin
declare result integer;
	IF EXISTS(SELECT book_id
                        FROM inventory
                        WHERE book_id = bid)
      THEN 
            SET result = 1;
      ELSE
            SET result = 0;
      END IF;
      return result;
end$$
DELIMITER ;


DELIMITER $$
create function checkFinancial(uname varchar(30), bid varchar(5))
returns integer deterministic
begin
declare result integer;
	IF (SELECT account_balance
                        FROM systematic_account
                        WHERE uname = user_name) - 0.05 *(SELECT price
											FROM book
											WHERE book_id = bid) > 0
      THEN 
            SET result = 1;
      ELSE
            SET result = 0;
      END IF;
      return result;
end$$
DELIMITER ;



DELIMITER $$
create function checkWarnings(uname varchar(30))
returns integer deterministic
begin
declare result integer;
	IF (SELECT warning
                        FROM systematic_account
                        WHERE uname = user_name) < 4
      THEN 
            SET result = 1;
      ELSE
            SET result = 0;
      END IF;
      return result;
end$$
DELIMITER ;


DELIMITER $$
create function checkRightBook(uname varchar(30),bid varchar(5))
returns integer deterministic
begin
declare result integer;
	
    if (select type_of_account
		from systematic_account natural join personal_account
        where uname = user_name) = 'normal' then
        if (select category
			from book
            where bid = book_id ) != 'uni' and 'ref' 
			then 
				set result = 1;
		else
				set result = 0;
		end if;
	elseif (select type_of_account
			from systematic_account natural join personal_account
			where uname = user_name) = 'student' then
			if (select category
				from book
				where bid = book_id ) != 'ref' 
				then 
					set result = 1;
			else
					set result = 0;
			end if;
	else
		set result = 1;
        
	end if;
    
	return result;
end$$
DELIMITER ;


DELIMITER $$
create procedure borrowBook(uname varchar(30), bid varchar(5))
DETERMINISTIC
	begin
		if checkWarnings(uname) != 0 and checkFinancial(uname, bid) != 0 and checkBookExistance(bid) != 0 and checkRightBook(uname, bid) != 0
        then
			update systematic_account, book
            set systematic_account.account_balance = systematic_account.account_balance - book.price * 0.05
            where uname = user_name and book_id = bid;
            
            update inventory
            set quantity = quantity - 1
            where bid = book_id;
            
            delete from inventory, book using inventory natural join book where quantity<1 and bid=book_id;
            ##get id
            insert into history(id, book_id, result, start_date) values (getId(uname),bid, 'success', CURDATE());
            
            insert into inbox(message) values (CONCAT('in ', CURDATE(), ' user ', getId(uname), ' borrowed book ', bid, ' succesfully'));
		else
			if checkBookExistance(bid) = 0
             then
				insert into history(id, book_id, result, start_date) values (getId(uname),bid, 'DOESNT EXIST', CURDATE());
			elseif checkFinancial(uname, bid) = 0
		       then
                 insert into history(id, book_id, result, start_date) values (getId(uname),bid, 'NO MONNEY', CURDATE());
			   
			elseif  checkWarnings(uname) = 0 then
				insert into history(id, book_id, result, start_date) values (getId(uname),bid, 'WARNING', CURDATE());
                
			else
				insert into history(id, book_id, result, start_date) values (getId(uname),bid, 'wrong choice', CURDATE());
                end if;
	    end if;
	end$$
DELIMITER ;



DELIMITER $$
create function getId(uname varchar(30))
returns varchar(3) deterministic
begin
declare result varchar(3);
	
    set result = (select distinct id
    from systematic_account
    where uname = user_name);
	
	return result;
end$$
DELIMITER ;



DELIMITER $$
create procedure deleteAccount(IN uname varchar(30))
	deterministic
    begin
		SET FOREIGN_KEY_CHECKS=0;
		delete from personal_account, systematic_account, user_address, user_phone
        using systematic_account natural join personal_account natural join user_address natural join user_phone
        where id = getId(uname);
        SET FOREIGN_KEY_CHECKS=1;
	end$$
DELIMITER ;


# these two procedures are for management views
DELIMITER $$
create procedure seeHistory()
	deterministic
    begin
		select *
        from history
        order by start_date desc;
	end$$
DELIMITER ;
DELIMITER $$
create procedure seeUsers()
	deterministic
    begin
		select *
        from personal_account natural join user_phone natural join user_address;
	end$$
DELIMITER ;


#liste darkhast haye success shode
DELIMITER $$
create procedure successfulResults()
	deterministic
    begin
		select *
        from history
        where result = 'success';
	end$$
DELIMITER ;


DELIMITER $$
create procedure returnBook(IN uname varchar(30), IN bid varchar(5),IN returned varchar(30))
	deterministic
    begin
		update history
        set returned_date = returned
        where book_id = bid and result = 'success' and getId(uname) = id and returned_date is null and history_id is not null;
	end$$
DELIMITER ;


DELIMITER $$

CREATE TRIGGER after_returned_update
AFTER UPDATE
ON history FOR EACH ROW 
BEGIN
    
    # update systematic_account set warning = 0;
    if (select distinct DATEDIFF(new.returned_date , new.start_date))
													> (select distinct available_date
													  from inventory
													  where new.book_id = book_id) then
		
        update systematic_account
        set warning = warning + 1
        where  new.id = systematic_account.id;
		insert into inbox(message) values (CONCAT('user ', (select id
															from systematic_account
                                                            where id=new.id), ' had delay'));
	else	
		insert into inbox(message) values (CONCAT('user ', (select id
															from systematic_account
                                                            where id=new.id), ' returned in time'));
	end if;
END$$
DELIMITER ;


show triggers;


#emtiazi
DELIMITER $$
create procedure bookHistory(IN bid varchar(5))
	deterministic
    begin
		select *
        from history
        where bid = book_id
        order by start_date desc;
	end$$
DELIMITER ;


DELIMITER $$
create procedure showInbox()
	deterministic
    begin
    select *
    from inbox;
    end$$
DELIMITER ;


DELIMITER $$
create procedure bookSearch4(IN input1 varchar(30), IN input2 varchar(30), IN input3 varchar(30),IN input4 varchar(30))
	deterministic
    begin
	
    if exists (select *
				from book
                where input1 in (title, author, edition, category) and input2 in (title, author, edition, category)
                 and input3 in (title, author, edition, category) and input4 in (title, author, edition, category)) 
                 then
                 select *
				from book
                where input1 in (title, author, edition, category) and input2 in (title, author, edition, category)
                 and input3 in (title, author, edition, category) and input4 in (title, author, edition, category)
                 order by title asc;
	else
		select 'this book doesnt exist! ';
        
	end if; 
                 
    end$$
DELIMITER ;

DELIMITER $$
create procedure bookSearch3(IN input1 varchar(30), IN input2 varchar(30), IN input3 varchar(30))
	deterministic
    begin
	
    if exists (select *
				from book
                where input1 in (title, author, edition, category) and input2 in (title, author, edition, category)
                 and input3 in (title, author, edition, category)) 
                 then
                 select *
				from book
                where input1 in (title, author, edition, category) and input2 in (title, author, edition, category)
                 and input3 in (title, author, edition, category)
                 order by title asc;
	else
		select 'this book doesnt exist! ';
        
	end if; 
                 
    end$$
DELIMITER ;

DELIMITER $$
create procedure bookSearch2(IN input1 varchar(30), IN input2 varchar(30))
	deterministic
    begin
	
    if exists (select *
				from book
                where input1 in (title, author, edition, category) and input2 in (title, author, edition, category)
                 ) 
                 then
                 select *
				from book
                where input1 in (title, author, edition, category) and input2 in (title, author, edition, category)
                order by title asc
                 ;
	else
		select 'this book doesnt exist! ';
        
	end if; 
                 
    end$$
DELIMITER ;


DELIMITER $$
create procedure bookSearch1(IN input1 varchar(30))
	deterministic
    begin
	
    if exists (select *
				from book
                where input1 in (title, author, edition, category)
                 ) 
                 then
                 select *
				from book
                where input1 in (title, author, edition, category)
                order by title asc
                 ;
	else
		select 'this book doesnt exist! ';
        
	end if; 
                 
    end$$
DELIMITER ;

DELIMITER $$
CREATE EVENT event1
	ON SCHEDULE EVERY '1' MONTH
	STARTS '2021-2-9'
	DO 
	BEGIN
		update systematic_account
        set warning = 0
        where  warning = 4; 
	END$$
DELIMITER ;


