�γ̣�MySQL��ϵ�����ݿ�
���ȣ�day2

�ϴ����ݻع�
1. ��������
1�����ݿ⣺����һ������ģ��
   ��ѧ����Ч�����ݽ��й���Ĳֿ�
2��DBMS�����ݿ����ϵͳ��ר���������ݹ����
   �����������Ҫ�У��������ݴ�ȡ�����ݰ�ȫ
   �ԡ��ɿ��ԣ�����/�ָ����ߡ����ܡ��Ѻõ�
   �û����桢�ḻ�ĳ���ӿ�
3��������ϵ�����ݿ⣺Oracle, MySQL, SQL Server,
   DB2
4�����ݹ��������׶Σ��˹��׶Σ��ļ�����
   ���ݿ����׶�
5������ģ�ͣ����ģ�ͣ���״ģ��
   ��ϵģ�ͣ�ʹ�ö�ά�����洢���ݡ�������ϵ
   �ǹ�ϵģ��
6����ϵģ����Ҫ�ĸ���
  - ��ϵ���淶�Ķ�ά�������Ʋ����ظ���
    ���Բ����ٷ֡����ݵĴ��򲢲���Ҫ��
  - ʵ�壺��ʵ�������ֵ�����
  - Ԫ�飺���е�һ������
  - ���ԣ�ʵ�����������
  - ������������ʵ������ԡ��������
  - �����������еļ��У�ѡȡһ����Ϊ����
    �ڹ�ϵ����Ϊ�߼���Ψһ����ʵ�������
	Ҫ��ǿա�Ψһ

2. MySQL����
1����װ
2���������
  - ������/etc/init.d/mysql start
    ֹͣ��stop����
	�鿴״̬��status����
  - �鿴�˿ڣ�netstat -an | grep 3306
3�������
  - �鿴�⣺show databases;
  - ����⣺use ����;
  - �����⣺create DATABASE ���� [�ַ���];
  - �鿴���еı�show tables;
4�������
  - ������
    CREATE TABLE ����(
		�ֶ�1 ����(����),
		�ֶ�2 ����(����),
        ......
	);
  - �鿴��ṹ��desc ����;
  - �鿴������䣺show CREATE TABLE ����

5�����ݹ���
  - ����
    INSERT INTO orders
	values('20180101','C0001',now(),1,1,100)

    INSERT INTO orders(order_id, cust_id)
	values('20180101','C0001')

    INSERT INTO orders(order_id, cust_id)
	VALUES('20180101','C0001'),
	      ('20180102','C0002');

  - ��ѯ
    SELECT * FROM orders;
	SELECT order_id, cust_id FROM orders;
	SELECT * FROM orders WHERE cust_id='C0001';
	
	SELECT * FROM orders
	WHERE cust_id = 'C0001'
	AND status = 1;

���������

��������
1. ��ֵ����
  - �����ͣ�TINYINT, INT, BITINT
  - ������: DECIMAL(16, 2)

  ʹ��ע�⣺����Ҫע��洢��Χ
            ������Ҫע�⾫��

  ��ϰ��
  ��һ�������������������ֶΣ����͡������ͣ� 
  CREATE TABLE num_test(
    -- type�������ͣ��洢ʵ�ʿռ���4Bytes
    -- ��С�����������;�����
    -- INT(3)��ʾĬ����ʾ3λ
    -- unsigned��ʾ�޷��ţ�0��������
    -- zerofill��ʾ�����0���
	type INT(3) unsigned zerofill,
	rate DECIMAL(10,2)
  );

  �ڶ������������� 
  -- ����ֵ
  INSERT INTO num_test VALUES(1, 0.88);
  -- С�����ֳ������峤��
  INSERT INTO num_test VALUES(2, 123.456);
  -- �������ֶβ�������
  INSERT INTO num_test VALUES(3, 2);
  -- �������������ʾ���
  INSERT INTO num_test VALUES(1000,3.444);
  
2. �ַ�����
1�������ַ�(CHAR)
  - ���洢255���ַ�
  - ���峤�Ⱥ�������ݲ��㣬�Զ�����ո�
  - ���������޷�����
  - ��������ó��ȣ�Ĭ�ϳ���Ϊ1
2���䳤�ַ�(varchar)
  - ���洢65535���ֽ�
  - ʵ�ʴ洢�ռ����ʵ�����ݽ��з���
  - ���ȳ������峤��ʱ�޷�����
3�����ı�����(TEXT)
  - �ܴ洢����65535�ַ�������
  - �����Դ洢4G������

3. ö��
1��ENUM���Ӹ����ļ���ֵ��ѡȡ1��
2��SET: �Ӹ�����ֵ��ѡȡ1������
3��ʾ����
  CREATE TABLE enum_test(
    name VARCHAR(32),
	sex  enum('boy','girl'),
	course SET('music','dance','paint')
  );
  INSERT INTO enum_test 
  VALUES('Jerry','girl','music,dance');
  -- ������Χ������
  INSERT INTO enum_test 
  VALUES('Tom','boy','music,football');

4. ����ʱ������
1�����ڣ�DATE����Χ'1000-01-01'~'9999-12-31'
2��ʱ�䣺TIME
3������ʱ������
4��ʱ������ͣ�TIMESTAMP
5��ʾ��
  SELECT now(), sysdate(); -- ȡ��ǰʱ��
  SELECT curdate(), curtime(); -- ȡ��ǰ���ڡ�ʱ��
  -- �ֱ�ȡ����ǰʱ���е��ꡢ�¡���
  SELECT YEAR(now()),MONTH(now()),DAY(now());
  -- ȡ����ǰϵͳʱ�������ڡ�ʱ�䲿��
  SELECT DATE(now()), TIME(now());

�޸ļ�¼
1. �﷨
   UPDATE ����
   SET �ֶ�1 = ֵ1,
       �ֶ�2 = ֵ2,
	   ...
   WHERE �������ʽ;
2. ʾ��
  - �޸�ĳ��������״̬
  UPDATE orders SET status = 2
  WHERE order_id = '201801010001';

  - �޸Ķ�������Ʒ�����Ͷ������
  UPDATE orders 
     SET products_num = 2,
	     amt = 400
   WHERE order_id = '201801010002';

ɾ����¼
1. �﷨
  DELETE FROM ���� WHERE �������ʽ;
2. ʾ��
  -- ɾ��201801010002��������Ϣ
  DELETE FROM orders 
  WHERE order_id = '201801010002';
3. �ر�ע��
  1�������ϸ������޶��������������ɾ������
  2����ʵ��Ŀ�У�ɾ�����޸�����֮ǰһ��Ҫ����

�����ѯ
1. ���Ƚϲ������Ĳ�ѯ��>,<,>=,<=,<>(��!=)
  ʾ��1����ѯ���ж���������200Ԫ�Ķ���
  SELECT * FROM orders WHERE amt > 200;

  ʾ��2����ѯ����״̬��Ϊ2�Ķ���
  SELECT * FROM orders WHERE status <> 2;

2. �߼��������AND��OR
  - and: �������ͬʱ����
  - or: ��������һ��

  ʾ������ѯ�ͻ����ΪC0002��C0003������
        ����״̬Ϊ1�Ķ���
  SELECT * FROM orders
  WHERE (cust_id='C0002' OR cust_id='C0003')
  AND status = 1;

3. ��Χ�Ƚ�
1��between...AND...: ��...��...֮��(��������)
2��in/NOT in: ��/����ĳ��ָ���ķ�Χ
3��ʾ��
  ʾ��1���������н����200~300֮��Ķ���
  SELECT * FROM orders 
  WHERE amt BETWEEN 200 AND 300;

  ʾ��2����ѯ�ͻ������('C0003','C0004')
         ��Χ�ڵĶ���
  SELECT * FROM orders
  WHERE cust_id IN ('C0003','C0004');
  -- where status in(1,2,3)
  -- NOT IN ��ʾcust_id����ָ����Χ��

4. ģ����ѯ
1����ʽ��where �ֶ� LIKE "ͨ���ַ�"
2��ͨ���ƥ��
   �»���(_): ƥ�䵥���ַ�
   �ٷֺ�(%): ƥ��������ַ�
3��ʾ��
  ��һ�������ͻ���Ϣ��
  CREATE TABLE customer(
    cust_id VARCHAR(32),
	cust_name VARCHAR(32),
	tel_no VARCHAR(32)
  ) DEFAULT charset=utf8;
  �ڶ����������������
  INSERT INTO customer VALUES
  ('C0001','Jerry','13512345678'),
  ('C0002','Dekie','13522334455'),
  ('C0003','Dokas','15844445555');
  ��������ģ����ѯ
  -- ��ѯ����������D��ͷ�Ŀͻ�
    SELECT * FROM customer 
	WHERE cust_name LIKE 'D%';
  -- ��ѯ���е绰�����а���44��55
    SELECT * FROM customer
	WHERE tel_no LIKE '%44%55%';
4��ע�����
   ģ����ѯ����ȷƥ�䣬�ٶȽ���
   ��������%ǰ��

5. ��ֵ���ǿ��ж�
1���﷨
   �жϿ�ֵ���ֶ� IS NULL
   �жϷǿգ��ֶ� IS NOT NULL
2��ʾ������ѯ�绰����Ϊ��ֵ�Ŀͻ���Ϣ
  SELECT * FROM customer
  WHERE tel_no IS null;
  -- where tel_no is not null; -- �绰�ǿ�

��ѯ�Ӿ�
1. ORDER BY: ����
1����ʽ��order BY �ֶ� [ASC/DESC]
   ASC-����    DESC-����
2��ʾ������ѯ���ж��������ս�������
  SELECT order_id, amt 
  FROM orders
  ORDER BY amt desc;  -- asc��д������

2. limit�Ӿ�
1�����ã�������ʾ�ı���
2����ʽ
   limit n     ֻ��ʾǰ��n��
   limit m,n   �ӵ�m��ʼ���ܹ���ʾn��
3��ʾ��
   -- ��ѯ���ж�������ʾǰ2��
   SELECT * FROM orders limit 2;
   -- ��ѯ���ж�������ʾ�������2��
   SELECT * FROM orders 
   ORDER BY amt DESC limit 2;
   
   -- ����limit��ҳ��ÿҳ3������
   -- ��1ҳ
   SELECT * FROM customer limit 0,3;
   -- ��2ҳ
   SELECT * FROM customer limit 3,3;
   -- ��3ҳ
   SELECT * FROM customer limit 6,3;

3. distinct�Ӿ�
1�����ã�ȥ���ظ�����
2���﷨��ʽ
    SELECT DISTINCT(Ҫȥ�ص��ֶ�)
	FROM ����
3��ʾ������ѯ�ͻ�����һ���м������ظ�������
    SELECT DISTINCT(cust_name)
	FROM customer;

4. �ۺϺ���
1��ʲô�Ǿۺϣ�����ֱ�Ӳ�ѯ���е����ݣ�
   ���Ƕ����ݽ����ܽᣬ���ؽ��
2���ۺϺ����У�
   max     �����ֵ
   MIN     ����Сֵ
   AVG     ��ƽ��ֵ
   SUM     ���
   COUNT   ͳ�Ʊ���
3��ʾ��
   SELECT MAX(amt) "�����",
          MIN(amt) "��С���",
		  AVG(amt) "ƽ�����",
		  SUM(amt) "�����ܽ��"
   FROM orders;

   -- ͳ�ƶ�������
   SELECT COUNT(*) FROM orders;

   -- ͳ�Ƶ绰������135��ͷ�Ŀͻ�����
   -- ��customer��
   SELECT COUNT(*) FROM customer
   WHERE tel_no LIKE '135%';

   ˵������ĳ���ֶε��þۺϺ���ʱ�����
         �ֶε�ֵΪ�գ��������ۺϲ���

4. ���飺group BY
1�����ã��Բ�ѯ������з��飬ͨ���;ۺϺ���
   ����ʹ��
2���﷨��ʽ��group BY �ֶ�
3��ʾ��
   -- ͳ�ƿͻ����������տͻ����Ʒ���
   SELECT cust_name, COUNT(*)
   FROM customer GROUP BY cust_name;

   -- ��orders��ͳ��ÿ��״̬�������ܽ��
   SELECT status, SUM(amt) 
   FROM orders GROUP BY status; 

5. Having���Է��������й���
1�����ã��Է��������й��ˣ���Ҫ��group BY
   ������ʹ��
2���﷨��ʽ
   GROUP BY �����ֶ� HAVING ��������
3��ʾ��
   -- ���ն���״̬ͳ���ܽ��
   -- ��ѯ�����ֻ�����ܽ�����500��
   SELECT status, SUM(amt) 
   FROM orders 
   GROUP BY status
   HAVING SUM(amt) > 500;

   ˵����group by����ۺϵĽ����ֻ����
         having��������where��whereֻ��
		 �û������е��ֶ���Ϊ����ʱ��

��ṹ����
1. ����ֶ�
1���﷨
  - ��ӵ�������һ���ֶ�
   ALTER table ���� ADD �ֶ��� ����(����) 
  - ��ӵ���ĵ�һ���ֶ�
   ALTER table ���� ADD �ֶ��� ����(����) first
  - ָ����ӵ�ĳ���ֶκ���
   ALTER table ���� ADD �ֶ��� ����(����) 
   after �ֶ�����
2��ʾ��
  CREATE TABLE student(
    stu_no VARCHAR(32),
	stu_name VARCHAR(128)
  );
  ����ֶ�
  -- �������������ֶ�
  ALTER TABLE student ADD age int;
  -- ��id�ֶ���ӵ���һ���ֶ�
  ALTER TABLE student ADD id INT first;
  -- ��tel_no��ӵ�stu_name����
  ALTER TABLE student ADD tel_no VARCHAR(32)
  after stu_name;
  
2. �޸��ֶ�
1���޸��ֶ�����
  ALTER TABLE ���� modify �ֶ� ����(����)
2���޸��ֶ�����
  ALTER TABLE ���� 
  change ���ֶ��� ���ֶ��� ����(����)
3��ʾ��
  -- �޸�student��stu_name�ֶγ���Ϊ64
  ALTER TABLE student 
  modify stu_name VARCHAR(64);

  -- ��student��age�ֶθ�Ϊstu_age
  ALTER TABLE student
  change age stu_age int;

3. ɾ���ֶ�
1���﷨��ALTER TABLE ���� DROP �ֶ���
2��ʾ����ɾ��student��id�ֶ�
  ALTER TABLE student DROP id;





