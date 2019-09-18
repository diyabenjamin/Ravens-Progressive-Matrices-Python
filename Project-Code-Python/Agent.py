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
from PIL import Image, ImageChops, ImageDraw


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
        for i in range(1, 7):
            image_numbers[i] = Image.open(problem.figures[str(i)].visualFilename)

        image_a = Image.open(problem.figures['A'].visualFilename)
        image_b = Image.open(problem.figures['B'].visualFilename)
        image_c = Image.open(problem.figures['C'].visualFilename)

        # if A, B and C are same, get the answer that is same as B
        diff_ab = ImageChops.difference(image_a, image_b)
        diff_ac = ImageChops.difference(image_a, image_c)
        diff = ImageChops.difference(diff_ab, diff_ac)
        if not diff.getbbox():
            print 'A, B, C are same'
            for i in range(1, 7):
                if not ImageChops.difference(image_b, image_numbers[i]).getbbox():
                    return i

        # if A and C are same or if A and B are same
        if self.get_similarity_ratio(image_a, image_c) > 0.98:
            print 'A and C are same'
            index = 0
            curr_max_val = 0
            for i in range(1, 7):
                similarity_ratio = self.get_similarity_ratio(image_b, image_numbers[i])
                if similarity_ratio > 0.98 and similarity_ratio > curr_max_val:
                    index = i
                    curr_max_val = similarity_ratio
            if index > 0:
                return index
        elif self.get_similarity_ratio(image_a, image_b) > 0.98:
            print 'A and B are same'
            index = 0
            curr_max_val = 0
            for i in range(1, 7):
                similarity_ratio = self.get_similarity_ratio(image_c, image_numbers[i])
                if similarity_ratio > 0.98 and similarity_ratio > curr_max_val:
                    index = i
                    curr_max_val = similarity_ratio
            if index > 0:
                return index

        # Transposed flip left to right image A same as B
        image_at = image_a.transpose(Image.FLIP_LEFT_RIGHT)
        image_ct = image_c.transpose(Image.FLIP_LEFT_RIGHT)

        similarity_ratio_atb = self.get_similarity_ratio(image_at, image_b)
        index = 0
        curr_max_val = 0
        if similarity_ratio_atb > 0.98:
            # and self.rms_difference(image_at, image_b) < 5:
            print 'flip left-right A and B are same'
            for i in range(1, 7):
                similarity_ratio_ctnumbers = self.get_similarity_ratio(image_ct, image_numbers[i])
                if similarity_ratio_ctnumbers > 0.97 and similarity_ratio_ctnumbers > curr_max_val:
                    index = i
                    curr_max_val = similarity_ratio_ctnumbers
            if index > 0:
                return index

        # Transposed flip left to right image A same as C
        image_at = image_a.transpose(Image.FLIP_TOP_BOTTOM)
        image_bt = image_b.transpose(Image.FLIP_TOP_BOTTOM)
        similarity_ratio_atc = self.get_similarity_ratio(image_at, image_c)
        index = 0
        curr_max_value = 0
        if similarity_ratio_atc > 0.98:
            print 'flip left-right A and C are same'
            for i in range(1, 7):
                similarity_ratio_btnumbers = self.get_similarity_ratio(image_bt, image_numbers[i])
                if similarity_ratio_btnumbers > 0.97 and similarity_ratio_btnumbers > curr_max_value:
                    index = i
                    curr_max_value = similarity_ratio_btnumbers
            if index > 0:
                return index

        # Rotate A from 45 to 315 is same as C or same as B
        for k in range(1, 8):
            image_ar = image_a.convert('L').point(lambda i: i < 150 and 255).rotate(45 * k)
            image_br = image_b.convert('L').point(lambda i: i < 150 and 255).rotate(45 * k)
            image_cr = image_c.convert('L').point(lambda i: i < 150 and 255).rotate(45 * k)
            similarity_ratio_arc = self.get_similarity_ratio(image_ar, image_c.convert('L').point(
                lambda i: i < 150 and 255))
            similarity_ratio_arb = self.get_similarity_ratio(image_ar, image_b.convert('L').point(
                lambda i: i < 150 and 255))
            index = 0
            max_ratio = 0
            if similarity_ratio_arc > 0.97:
                print 'A rotate and C are same'
                for i in range(1, 7):
                    image_num_r = image_numbers[i].convert('L').point(lambda i: i < 150 and 255)
                    similarity_ratio_brnumbers = self.get_similarity_ratio(image_br, image_num_r)
                    if similarity_ratio_brnumbers > 0.97 and similarity_ratio_brnumbers > max_ratio:
                        index = i
                        max_ratio = similarity_ratio_brnumbers
                if index > 0:
                    return index
            elif similarity_ratio_arb > 0.97:
                print 'A rotate and B are same'
                for i in range(1, 7):
                    image_num_r = image_numbers[i].convert('L').point(lambda i: i < 150 and 255)
                    similarity_ratio_crnumbers = self.get_similarity_ratio(image_cr, image_num_r)
                    if similarity_ratio_crnumbers > 0.96 and similarity_ratio_crnumbers > max_ratio:
                        index = i
                        max_ratio = similarity_ratio_crnumbers
                if index > 0:
                    return index

        # Basic B-10/B-11
        diff_image = ImageChops.invert(ImageChops.difference(image_a, image_b))
        new_image = ImageChops.invert(ImageChops.difference(image_c, diff_image))
        option = 0
        max_similarity_ratio = 0
        for i in range(1, 7):
            similarity_ratio = self.get_similarity_ratio(new_image, image_numbers[i])
            if round(similarity_ratio, 2) >= 0.97 and similarity_ratio > max_similarity_ratio:
                option = i
                max_similarity_ratio = similarity_ratio

        if option > 0:
            print 'Challenge B-09/ Basic B-10/B-11', max_similarity_ratio
            return option

        # Basic B-09
        new_image_a = self.fill_image(image_a)
        similarity_ratio_a_b = self.get_similarity_ratio(new_image_a, image_b)

        if round(similarity_ratio_a_b, 2) >= 0.97:
            option = 0
            max_similarity_ratio = 0
            for i in range(1, 7):
                new_image_c = self.fill_image(image_c)
                similarity_ratio = self.get_similarity_ratio(new_image_c, image_numbers[i])
                if round(similarity_ratio, 2) >= 0.97 and similarity_ratio > max_similarity_ratio:
                    option = i
                    max_similarity_ratio = similarity_ratio

            if option > 0:
                print 'Fill image - Basic B-09'
                return option

        return -1

    def get_binary_images(self, image1):
        image_l = image1.convert('L')
        img_binary = np.array(image_l)
        img_binary[img_binary < 128] = 1
        img_binary[img_binary >= 128] = 0
        return img_binary

    def get_similarity_ratio(self, img1, img2):
        binary_img1 = self.get_binary_images(img1)
        binary_img2 = self.get_binary_images(img2)
        rows = binary_img1.shape[0]
        columns = binary_img1.shape[1]
        difference_matrix = np.zeros((rows, columns), dtype=float)
        for i in xrange(rows):
            for j in xrange(columns):
                difference_matrix[i][j] = abs(float(binary_img1[i][j]) - float(binary_img2[i][j]))
        difference_ratio = np.sum(difference_matrix) / float(rows * columns)
        return 1 - difference_ratio

    def fill_image(self, image):
        image_copy = image.copy()
        width, height = image_copy.size
        center = (int(0.5 * width), int(0.5 * height))
        ImageDraw.floodfill(image_copy, xy=center, value=(0, 0, 0, 0))
        return image_copy
