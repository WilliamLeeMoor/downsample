import cv2 as cv
import sys
import numpy as np

full_res_height = 2196
full_res_width = 3864
work_res_height = 366
work_res_width = 644

def downsample(DownsampleKernelWidth, DownsampleKernelHeight, sigmaFactor, BaseImg, filename):
    sigmaX = 0.3 * ((DownsampleKernelWidth - 1) * 0.5 - 1) + 0.8
    sigmaY = 0.3 * ((DownsampleKernelWidth - 1) * 0.5 - 1) + 0.8
    sigmaX *= sigmaFactor
    sigmaY *= sigmaFactor
    print("Downsampling with a %dx%d kernel and sigma=(%.2f,%.2f)..." % (DownsampleKernelWidth, DownsampleKernelHeight, sigmaX, sigmaY))
    BlurredFullRes = cv.GaussianBlur(BaseImg,(DownsampleKernelWidth,DownsampleKernelHeight),sigmaX,sigmaY)
    Downsampled = cv.resize(BlurredFullRes, (work_res_width, work_res_height))
    OutFileName = "downsampled_" + filename
    #cv.imshow(OutFileName, Downsampled)
    cv.imwrite(OutFileName, Downsampled)

def run_downsampling(filename):
    print("Input file: " + filename)
    img = cv.imread(filename)

    if img is None:
        print("Invalid image: " + sys.argv[i + 1] + ". Skipping...")
        return
    if img.shape[0] != full_res_height or img.shape[1] != full_res_width:
        print("Invalid image: " + sys.argv[i+1] + ". Skipping...")
        print("Dimension: %d x %d; Desired: %d x %d" % (img.shape[0], img.shape[1], full_res_height, full_res_width))
        return

    #cv.imshow("Base image: " + filename, img)

    if(img.shape[0] != full_res_height or img.shape[1] != full_res_width):
        print("CAUTION: invalid image input size.")

    DownsampleRatioWidth = int(full_res_width / work_res_width)
    DownsampleRatioHeight = int(full_res_height / work_res_height)

    # Kernels can be bigger than the ratio because it can simple zero out the
    # weights for the edges of the kernel
    DownsampleKernelWidth = DownsampleRatioWidth + 1
    DownsampleKernelHeight = DownsampleRatioHeight + 1
    # Kernels have to be odd in size
    if(DownsampleKernelWidth % 2 == 0):
        DownsampleKernelWidth += 1;
    if(DownsampleKernelHeight % 2 == 0):
        DownsampleKernelHeight += 1;

    #downsample(DownsampleKernelWidth, DownsampleKernelHeight, 1, img)
    #downsample(15, 15, 1, img)
    #downsample(31, 31, 1, img)

    kernelSizesToTest = [7]
    sigmaValuesToTest = [1]

    for k in kernelSizesToTest:
        for s in sigmaValuesToTest:
            downsample(k, k, s, img, filename)


num_images = len(sys.argv)-1

if(cv.__version__ != "4.1.1"):
    print("CAUTION: You are not using the same OpenCV version as MoonRanger Flight. You may generate incorrect images.")

for i in range(num_images):
    run_downsampling(sys.argv[i+1]);

cv.waitKey(0)
