import commands
import sys

m = 0
o = 0
n = 0
k = 0
name = sys.argv[1]
for i in range(1,23):
	cmds = "zcat %s.%s.prism.phased.vcf.gz|grep '1|0'|wc -l" %(name,i)
	a=int(commands.getoutput(cmds).strip())
	cmds = "zcat %s.%s.prism.phased.vcf.gz|grep '0|1'|wc -l" %(name,i)
	b=int(commands.getoutput(cmds).strip())
	m+=a+b
	mask = '%s_%s.mask.bed.gz' %(name,i)
	c=int(commands.getoutput("zcat %s|awk '{sum+=$3-$2} END {print sum}'" %(mask)).strip())
	vcf = '%s.%s.vcf.gz' %(name,i)
	d= int(commands.getoutput("zcat %s|grep '0/1\|1/0'|wc -l" %(vcf)).strip())
	vcf = '%s.%s.phased.vcf.gz' %(name,i)
	e= int(commands.getoutput("zcat %s|grep '0|1\|1|0'|wc -l" %(vcf)).strip())
	o+=c
	n+=d
	print i,c,d,a+b,e
	k+=e
print o,m,n,float(m)/n,k
