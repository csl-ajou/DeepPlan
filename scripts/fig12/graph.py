#!/usr/bin/env python
# coding: utf-8

# In[3]:

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import gridspec
import sys
import os
import csv

def get_data(target):
    target = "{}/bert_base_{}".format(sys.argv[1], target)
    target = target.strip()
    if target[0] != '/':
        target = os.path.join(os.getcwd(), target)

    latency = np.array([])
    goodput = np.array([])
    cold = np.array([])

    result = []

    with open(target, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        for i, line in enumerate(rdr):
            latency = np.append(latency, float(line[0]))
            goodput = np.append(goodput, float(line[1]))
            cold = np.append(cold, float(line[2]))

        result.append(latency)
        result.append(goodput)
        result.append(cold)

        return result

x_value = [20 * i for i in range(1, 11)]


label_list = ["PipeSwitch", "DeepPlan (DHA)", "DeepPlan (PT+DHA)"]
# color_list = ['#AEB6BF', '#5D6D7E', '#34495E', '#273746', '#273746']
color_list = ['#AEB6BF', '#5D6D7E', '#273746']
marker_list = ['o', '^', 'P']
line_list = ['-', 'dotted', 'dashed']

# Prepare these files
engine_list = ["pipeline.csv", "deepplan.csv", "deepplan+.csv"]

ylim_list = {
            "bert_base": [(0, 300), (30, 105), (0, 60)],
            "bert_large": [],
            "roberta_base": [],
            "roberta_large": [],
            "gpt2": [],
            "gpt2_medium": []}


x_label = "# of model instances (concurrency)"
y_label = ["99 % latency (ms)", "Goodput (%)", "Cold-start (%)"]

FONTSIZE_LABEL = 16
FONTSIZE_TICK = 13
FONTSIZE_LEGEND = 14
SIZE_FIGURE = (7, 7)
LINE_WIDTH = 3
ARKER_SIZE = 10
MARKER_SIZE = 10


plt.figure(figsize=SIZE_FIGURE)
gs = gridspec.GridSpec(nrows=3,
                       ncols=1,
                       height_ratios=[1, 0.8, 0.8]
                      )

li_ax = []
for i in range(0, 3):
    li_ax.append(plt.subplot(gs[i]))

for i, engine in enumerate(engine_list):
    result = get_data(engine)

    for j, ax in enumerate(li_ax):

        ax.plot(x_value, result[j], linewidth = LINE_WIDTH, color=color_list[i], marker=marker_list[i], linestyle=line_list[i], markersize=MARKER_SIZE)

        ax.set_ylim(ylim_list["bert_base"][j])
        ax.tick_params(axis='both', labelsize=FONTSIZE_TICK)

        ax.set_xticks(x_value)
        if j < 2:
            ax.axes.xaxis.set_ticklabels([])
            ax.set_ylabel(y_label[j], fontsize=FONTSIZE_LABEL, labelpad=10)
        else:
            ax.set_ylabel(y_label[j], fontsize=FONTSIZE_LABEL, labelpad=18)


        if j == 0:
            ax.axhline(y=100, color='gray', linestyle='--')
            ax.text(20, 150, "Target SLO", fontsize=FONTSIZE_TICK)

        ax.grid(alpha=0.5, linestyle='--')

plt.legend(labels=label_list, bbox_to_anchor=(0.43, 3.55), ncol=3, loc='center', columnspacing=0.6,
           fontsize=FONTSIZE_LEGEND, edgecolor="#FFFFFF")

plt.xlabel(x_label, fontsize=FONTSIZE_LABEL, labelpad=10)

plt.subplots_adjust(hspace=0.06)
plt.rcParams["font.family"] = "Helvetica"
plt.savefig(sys.argv[2], bbox_inches="tight", pad_inches=0.0)

print("Saved graph to {}".format(sys.argv[2]))
