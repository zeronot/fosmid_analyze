#!/usr/bin/env python
# python plot_concordance_mec_cor.py
# Shiya Song
# 14 Jan 2015
# After using calc_concordance_mec_cor.py, draw plot

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pickle
import numpy as np
import matplotlib.patches as mpatches

def find_interval(pos,list):
	left = 0
	right = len(list)
	find = -1
	while right - left >0:
		midpoint = (right + left)/2
		if pos < list[midpoint]:
			right = midpoint
		elif pos > list[midpoint]:
			left = midpoint+1
		elif pos == list[midpoint]:
			left = midpoint
			find = midpoint
			break
		if pos<list[midpoint] and midpoint!=0:
			midpoint=midpoint-1
	return midpoint

def read_data(sample):
	dist_range = [0,5,10,100,1e06]
	LD_range = np.linspace(0,1,num=21)
	abundance1 = [[0 for x in range(len(LD_range))] for x in range(len(dist_range))] 
	genotype_concordance1 = [[[] for x in range(len(LD_range))] for x in range(len(dist_range))] 
	abundance2 = [[0 for x in range(len(LD_range))] for x in range(len(dist_range))] 
	genotype_concordance2 = [[[] for x in range(len(LD_range))] for x in range(len(dist_range))] 
	for chr in range(1,23):
		dbfile = open('/home/jmkidd/kidd-lab-scratch/shiya-projects/phased-genomes/phasing_compare/%s_chr%s_shapeit_1KGphase1_SNP_pair_pickle' %(sample,chr),'rb')
		Compare1 = pickle.load(dbfile)
		Compare2 = pickle.load(dbfile)
		list1 = Compare1.index
		list2 = Compare2.index
		for i in range(len(list1)):
			pos_dist = float(Compare1['dist'][list1[i]])/1000
			index_i = find_interval(pos_dist,dist_range)
			index_j = find_interval(Compare1['LD'][list1[i]],map(float,LD_range))
# print index_i,index_j,pos_dist,SNP["LD"][list[i]],SNP["MEC"][list[i]],SNP["clone_num"][list[i]]
			abundance1[index_i][index_j]+=1
			genotype_concordance1[index_i][index_j].append(Compare1['concord'][list1[i]])
		for i in range(len(list2)):
			pos_dist = float(Compare2['dist'][list2[i]])/1000
			index_i = find_interval(pos_dist,dist_range)
			index_j = find_interval(Compare2['LD'][list2[i]],map(float,LD_range))
# print index_i,index_j,pos_dist,SNP["LD"][list[i]],SNP["MEC"][list[i]],SNP["clone_num"][list[i]]
			abundance2[index_i][index_j]+=1
			genotype_concordance2[index_i][index_j].append(Compare2['concord'][list1[i]])
		print chr,'done'
	return abundance1,genotype_concordance1,abundance2,genotype_concordance2

def make_plot(abundance,genotype_concordance,MEC,clone_num):
	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	col = ['r','b','g','y','k']
	col2 = ['r--','b--','g--','y--','k--']
	label = ['<1 kbp','1-5 kbp','5-8 kbp','> 8kbp']
	for i in range(len(dist_range)-1):
		Genotype_concordance = []
		MEC_rate = []
		for j in range(len(LD_range)):
			if abundance[i][j]==0:
				Genotype_concordance.append(0)
				MEC_rate.append(0)
			else:
				Genotype_concordance.append(float(np.sum(genotype_concordance[i][j]))/abundance[i][j])
				MEC_rate.append(float(np.sum(MEC[i][j]))/np.sum(clone_num[i][j]))
				print i,j,abundance[i][j],float(np.sum(genotype_concordance[i][j]))/abundance[i][j],float(np.sum(MEC[i][j]))/np.sum(clone_num[i][j])
		print Genotype_concordance
		print MEC_rate
		ax2.plot(LD_range,MEC_rate,col2[i],label=label[i])
		ax1.plot(LD_range,Genotype_concordance,col[i],label=label[i])
	plt.axis([0, 1, 0, 0.03])
	ax1.set_xlabel("Pairwise SNP LD(D')")
	ax1.set_ylabel('percent agreement with\n shapeit phased haplotypes using 1KGphase3',multialignment='center')
	ax1.set_ylim([0,1])
	ax1.set_xlim([0,1])
	ax2.set_ylabel('MEC value per site',multialignment='center')
	ax2.set_ylim([0,0.08])
	plt.title('%s shapeit 1KGphase3' %(sample))
	ax1.legend(loc='center right')
	plot1, = plt.plot(2,2,'k')
	plot2, = plt.plot(3,3,'k--')
	plt.legend([plot1,plot2],['percent agreement','MEC value'],prop={'size':10})
	plt.savefig("/Users/songsy/Documents/Data/phase_compare/%s_shapeit_1KGphase3_concordance.pdf" %(sample),format='pdf')

def make_plot_v2(abundance,genotype_concordance,phase_panel,m):
	fig, ax1 = plt.subplots()
	col = ['r','b','g','y','k']
	label = ['<5 kbp','5-10 kbp','10-100 kbp','> 100kbp']
	for i in range(len(dist_range)-1):
		Genotype_concordance = []
		for j in range(len(LD_range)):
			if abundance[i][j]==0:
				Genotype_concordance.append(0)
			else:
				Genotype_concordance.append(float(np.sum(genotype_concordance[i][j]))/abundance[i][j])
				print i,j,abundance[i][j],float(np.sum(genotype_concordance[i][j]))/abundance[i][j]
		print Genotype_concordance
		ax1.plot(LD_range,Genotype_concordance,col[i],label=label[i])
	ax1.set_xlabel("Pairwise SNP LD(D')")
	ax1.set_ylabel('percent agreement with\n shapeit phased haplotypes using %s' %(phase_panel),multialignment='center')
	ax1.set_ylim([0,1])
	ax1.set_xlim([0,1])
	plt.title('%s shapeit %s' %(sample,phase_panel))
	ax1.legend(loc='lower right')
	plt.savefig("/home/jmkidd/kidd-lab-scratch/shiya-projects/phased-genomes/phasing_compare/%s_shapeit_%s_pair%s_concordance.pdf" %(sample,phase_panel,m),format='pdf')

if __name__=="__main__":
#	for sample in ['NA19240','NA21302','HG02799','HG03108','HG03428','NA20847']:
	for sample in ['NA19240']:
		abundance1,genotype_concordance1,abundance2,genotype_concordance2=read_data(sample)
		make_plot_v2(abundance1,genotype_concordance1,'1KGphase1','')
		make_plot_v2(abundance2,genotype_concordance2,'1KGphase1','_within_block')