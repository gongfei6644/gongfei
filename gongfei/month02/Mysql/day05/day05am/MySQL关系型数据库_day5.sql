�γ̣�MySQL��ϵ�����ݿ�
����: day5

�洢����
1. ʲô�Ǵ洢���棺�������ʵ�ַ�ʽ����������
   ʵ�ֲ�һ����������ͬ�洢�������͵ļ�������
   ��һ�������磺�洢���ƣ��������ƣ�������ʽ
2. �鿴�洢����
1���鿴MySQL֧�ֵĴ洢����:show engines;
2���鿴ĳ����Ĵ洢����
   show CREATE TABLE ������;
3���޸ı�Ĵ洢����
   ALTER TABLE ������ engine = ��������;
4��ʾ�������������޸Ĵ洢����
   CREATE TABLE t3 (
     id INT PRIMARY key,
	 name VARCHAR(32)
   ) engine = InnoDB;
   ALTER TABLE t3  engine=MyISAM;
   �鿴��show CREATE TABLE t3;

3.���ô洢�����ص�
1��InnoDB(MySQL5.5���Ժ�İ汾Ĭ��)
  - �ص㣺֧������֧���м�����֧�������
        �����ռ�

  - �ļ����ɣ�
    *.frm: ��Ľṹ������
	*.ibd: �������

  - ʵ�飺�鿴��Ĵ洢�ļ�
  ˵����ͨ�������ָ����Բ鿴���ݴ洢Ŀ¼
  show global variables like '%datadir%';

  ���Ȩ�޲�����ʹ��sudo -i ����root�û���
  ���������Ŀ¼�鿴

  cd /var/lib/mysql
  ls orders.*  (�鿴orders��Ĵ洢�ļ�)

  - ʲôʱ��ѡ��InnoDB:
    ����(��ɾ��)�����ܼ��ı�
	Ҫ��֧�����ݿ����������
	�Զ��ֱ��ͻָ���
	Ҫ��֧���Զ�����(auto_increment)�ֶΣ�

  - MyISAM
  �ص㣺֧�ֱ���������֧�����������������
        ��ռ��ռ䣻����洢���������𻵣�����
		�ֱ����ָ����ܲ���
  �ļ����ɣ�
    *.frm: ��ṹ
	*.myd: ����
	*.myi: ������
  ���ó��ϣ�
    ��ѯ����϶ࣻ
	����һ����Ҫ��ϵͣ�
	û�����Լ��Ҫ��

  - Memory
  �ص㣺��ṹ������̣����ݴ����ڴ���
        ������������ϵ�󣬱��е����ݶ�ʧ
  �ļ���*.frm   ��ṹ
  ʹ�ó��ϣ�������С��������Ҫ���ٷ��ʣ�
            ���ݶ�ʧ���������ʧ��
  ʵ�飺
  ��һ�����޸�t3�Ĵ洢����ΪMemory
    ALTER TABLE t3 engine=Memory;
  �ڶ������鿴�ļ�
    sudo -i
	cd /var/lib/mysql/eshop
	ls t3.*
  ������������һ�����ݣ���ѯ(���Կ�������)
    insert into t3 values(1,'Jerry');
  ���Ĳ������������ٲ�ѯ��������ʧ��
    /etc/init.d/mysql restart

pymysql��ʹ��
1. ȷ��pymysql���Ѿ���װ
  ����python����ģʽ��ִ��: import pymysql
  ���������˵���Ѱ�װ
 
  ���������������ѧ��
  ��orders��SQL���յ�һ�������

2. ɾ��orders����������
  DELETE FROM orders 
  WHERE cust_id > 'C00000005';









