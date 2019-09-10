# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
import numpy as np
from PIL import Image, ImageChops, ImageStat, ImageDraw


# import numpy

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        print problem.name

        image_numbers = [None] * 7
        buffer_numbers = [None] * 7
        for i in range(1, 7):
            image_numbers[i] = Image.open(problem.figures[str(i)].visualFilename)
            buffer_numbers[i] = np.asarray(image_numbers[i])

        image_a = Image.open(problem.figures['A'].visualFilename)
        image_b = Image.open(problem.figures['B'].visualFilename)
        image_c = Image.open(problem.figures['C'].visualFilename)

        buffer_a = np.asarray(image_a)
        buffer_b = np.asarray(image_b)
        buffer_c = np.asarray(image_c)

        diff_ab = ImageChops.difference(image_a, image_b)
        diff_ac = ImageChops.difference(image_a, image_c)
        diff = ImageChops.difference(diff_ab, diff_ac)

        if not diff.getbbox():
            print 'inside diff'
            for i in range(1, 7):
                if not ImageChops.difference(image_b, image_numbers[i]).getbbox():
                    return i

        # B-03
        if np.array_equal(buffer_a, buffer_c):
            print 'inside B-03'
            for i in range(1, 7):
                if np.array_equal(buffer_b, buffer_numbers[i]):
                    return i

        # B-04,05
        image_at = image_a.transpose(Image.FLIP_TOP_BOTTOM)
        image_bt = image_b.transpose(Image.FLIP_TOP_BOTTOM)
        diff_ratio_atc = self.get_difference(image_at, image_c)
        print diff_ratio_atc
        index = 0
        if diff_ratio_atc < 0.005:
            print 'inside B-05'
            for i in range(1, 7):
                if self.get_difference(image_bt, image_numbers[i]) <= diff_ratio_atc:
                    index = i
                    diff_ratio_atc = self.get_difference(image_bt, image_numbers[i])
            if index > 0:
                return index

        # Misc
        image_at = image_a.transpose(Image.FLIP_LEFT_RIGHT)
        image_ct = image_c.transpose(Image.FLIP_LEFT_RIGHT)

        diff_ratio_atb = self.get_difference(image_at, image_b)
        print diff_ratio_atb
        index = 0
        if diff_ratio_atb < 0.005:
            print 'inside Misc'
            for i in range(1, 7):
                if self.get_difference(image_ct, image_numbers[i]) <= diff_ratio_atb:
                    index = i
                    diff_ratio_atb = self.get_difference(image_ct, image_numbers[i])
            if index > 0:
                return index

        draw = ImageDraw.Draw(image_a)
        # draw.polygon([(0, 0), + image_a.size], fill=255)
        draw.polygon([0, image_a.size[0], image_a.size[1], image_a.size[1], image_a.size[1], 0], fill=128)
        del draw
        image_a.show()

        return -1

    def get_difference(self, image1, image2):
        diff_arc = ImageChops.difference(image1, image2)
        stat = ImageStat.Stat(diff_arc)
        diff_ratio = sum(stat.mean) / (len(stat.mean) * 255)
        return float(diff_ratio)

    def get_binary_images(self, image1):
        img_binary = np.asarray(image1).copy()
        img_binary[img_binary == 255] = 0
        img_binary[img_binary == 0] = 1
        return img_binary
