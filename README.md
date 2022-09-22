# FetalTransUNet

This repository includes the source code of the paper entitled: "Automatic Quality Assessment of First Trimester Crown-Rump-Length Ultrasound Images". This paper was submitted to ASMUS 2022 (a workshop held in conjunction with MICCAI 2022).

# Abstract

Fetal gestational age (GA) is vital clinical information that is estimated during pregnancy in order to assess fetal growth. This is usually performed by measuring the crown-rump-length (CRL) on an ultrasound image in the Dating scan which is then correlated with fetal age and growth trajectory. A major issue when performing the CRL measurement is ensuring that the image is acquired at the correct view, otherwise it could be misleading. Although clinical guidelines specify the criteria for the correct CRL view, sonographers may not regularly adhere to such rules. In this paper, we propose a new deep learning-based solu- tion that is able to verify the adherence of a CRL image to clinical guide- lines in order to assess image quality and facilitate accurate estimation of GA. We first segment out important fetal structures then use the local- ized structures to perform a clinically-guided mapping that verifies the adherence of criteria. The segmentation method combines the benefits of Convolutional Neural Network (CNN) and the Vision Transformer (ViT) to segment fetal structures in ultrasound images and localize important fetal landmarks. For segmentation purposes, we compare our proposed work with UNet and show that our CNN/ViT-based method outperforms an optimized version of UNet. Furthermore, we compare the output of the mapping with classification CNNs when assessing the clinical criteria and the overall acceptability of CRL images. We show that the proposed mapping is not only explainable but also more accurate than the best performing classification CNNs.


# Citation
Cengiz, S., Hamdi, I., Yaqub, M. (2022). Automatic Quality Assessment of First Trimester Crown-Rump-Length Ultrasound Images. In: Aylward, S., Noble, J.A., Hu, Y., Lee, SL., Baum, Z., Min, Z. (eds) Simplifying Medical Ultrasound. ASMUS 2022. Lecture Notes in Computer Science, vol 13565. Springer, Cham. https://doi.org/10.1007/978-3-031-16902-1_17

# Download Pre-trained Model

Link: Get the model -> https://console.cloud.google.com/storage/browser/vit_models?pli=1

# Data preparation 

 Data preparation should be completed according to "./datasets/README.md".
 This repo includes an example dataset includes GT, segmented and predicted of an ultrasound image. Check folder '''predictions'''.
 
# Environement 

'''cd ~TransUNet'''
'''pip install -r requirements.txt'''

# Run 

For train: 
'''python train.py --dataset Synapse --vit_name R50-ViT-B_16'''

For test: 
'''python test.py --dataset Synapse --vit_name R50-ViT-B_16 --save_nii

For criteria check: 
''' python pipelinecriteria.py ~/FetalTransUNet/predictions'''

It will automatically saves the CSV file.

# Credits
Please, cite. FetalTransUNet https://doi.org/10.1007/978-3-031-16902-1_17.
This code adopted TransUNet (https://doi.org/10.48550/arXiv.2102.0). 
