def foo():
    return [lambda x:i+x for i in range(4)]
print(foo())
print([x(3) for x in foo()])



���չ������ݣ�
1.ѧϰĽ����Django��Ŀ����Ҫ��ģ��ļ̳У�ǰ��ҳ�����ݷ�ҳչʾ�����20%����Ҫ�пγ̻�����չʾ��ɸѡ����