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
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HIGH_SIMILARITY_THRESHOLD = 0.98
LOW_SIMILARITY_THRESHOLD = 0.97


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

    image_numbers = [None] * 9
    image_a = None
    image_b = None
    image_c = None
    image_d = None
    image_e = None
    image_f = None
    image_g = None
    image_h = None

    def setup_global_variables(self, problem):
        self.image_a = Image.open(problem.figures['A'].visualFilename)
        self.image_b = Image.open(problem.figures['B'].visualFilename)
        self.image_c = Image.open(problem.figures['C'].visualFilename)
        image_numbers_count = 7

        if problem.problemType == '3x3':
            self.image_d = Image.open(problem.figures['D'].visualFilename)
            self.image_e = Image.open(problem.figures['E'].visualFilename)
            self.image_f = Image.open(problem.figures['F'].visualFilename)
            self.image_g = Image.open(problem.figures['G'].visualFilename)
            self.image_h = Image.open(problem.figures['H'].visualFilename)
            image_numbers_count = 9

        for i in range(1, image_numbers_count):
            self.image_numbers[i] = Image.open(problem.figures[str(i)].visualFilename)

    def Solve(self, problem):
        print problem.name
        option = -1

        self.setup_global_variables(problem)

        if problem.problemType == '2x2':
            option = self.solve_image_difference() if option == -1 else option
            option = self.solve_image_reflection() if option == -1 else option
            option = self.solve_image_rotation() if option == -1 else option
            option = self.solve_image_fill() if option == -1 else option
            option = self.solve_image_vertices_count() if option == -1 else option
            return option
        elif problem.problemType == '3x3':
            option = self.solve_similar_image_3x3() if option == -1 else option
            option = self.solve_similar_xy_axes_image_3x3() if option == -1 else option
            option = self.solve_triangular_image_pattern_3x3() if option == -1 else option
            option = self.solve_flip_image_pattern_3x3() if option == -1 else option
            option = self.solve_image_difference_3x3() if option == -1 else option
            option = self.solve_offset_images_3x3() if option == -1 else option
            # option = self.solve_dark_pixel_ratio_3x3() if option == -1 else option
            return option

    # 3x3 functions starts from here

    def solve_offset_images_3x3(self):
        image_a_o = ImageChops.offset(self.image_a, xoffset=self.image_a.width/2, yoffset=0)
        image_d_o = ImageChops.offset(self.image_d, xoffset=self.image_d.width/2, yoffset=0)
        image_g_o = ImageChops.offset(self.image_g, xoffset=self.image_g.width/2, yoffset=0)
        similarity_ao_c = self.get_similarity_ratio(image_a_o, self.image_c)
        similarity_do_f = self.get_similarity_ratio(image_d_o, self.image_f)
        max_ratio = 0
        index = 0
        if similarity_ao_c > 0.91 and similarity_do_f > 0.91:
            for i in range(1, 9):
                similarity_go_i = self.get_similarity_ratio(image_g_o, self.image_numbers[i])
                if similarity_go_i > 0.91 and similarity_go_i > max_ratio:
                    index = i
                    max_ratio = similarity_go_i
                if index > 0:
                    return index
        return -1

    def solve_similar_xy_axes_image_3x3(self):
        options = []
        g_xmin, g_xmax, g_ymin, g_ymax = self.get_x_and_y_values_images(self.image_g)
        h_xmin, h_xmax, h_ymin, h_ymax = self.get_x_and_y_values_images(self.image_h)
        c_xmin, c_xmax, c_ymin, c_ymax = self.get_x_and_y_values_images(self.image_c)
        f_xmin, f_xmax, f_ymin, f_ymax = self.get_x_and_y_values_images(self.image_f)

        if (
                self.is_same(g_xmin, h_xmin, 2) and
                self.is_same(g_xmax, h_xmax, 2) and
                self.is_same(c_ymin, f_ymin, 2) and
                self.is_same(c_ymax, f_ymax, 2)
        ):
            for i in range(1, 9):
                i_xmin, i_xmax, i_ymin, i_ymax = self.get_x_and_y_values_images(self.image_numbers[i])
                if (
                        self.is_same(i_xmin, h_xmin, 2) and
                        self.is_same(i_xmax, h_xmax, 2) and
                        self.is_same(i_ymin, f_ymin, 2) and
                        self.is_same(i_ymax, f_ymax, 2)
                ):
                    options.append(i)

        if len(options) == 1:
            print 'In similar xy axes images'
            return options[0]

        return -1

    def solve_similar_image_3x3(self):
        image_similarity_a_b = self.get_similarity_ratio(self.image_a, self.image_b)
        image_similarity_b_c = self.get_similarity_ratio(self.image_b, self.image_c)
        image_similarity_d_e = self.get_similarity_ratio(self.image_d, self.image_e)
        image_similarity_e_f = self.get_similarity_ratio(self.image_e, self.image_f)
        image_similarity_g_h = self.get_similarity_ratio(self.image_g, self.image_h)

        if (
                image_similarity_a_b >= LOW_SIMILARITY_THRESHOLD and
                image_similarity_b_c >= LOW_SIMILARITY_THRESHOLD and
                abs(image_similarity_a_b - image_similarity_b_c) <= 0.0001 and
                image_similarity_d_e >= LOW_SIMILARITY_THRESHOLD and
                image_similarity_e_f >= LOW_SIMILARITY_THRESHOLD and
                abs(image_similarity_d_e - image_similarity_e_f) <= 0.0001 and
                image_similarity_g_h >= LOW_SIMILARITY_THRESHOLD
        ):
            for i in range(1, 9):
                image_similarity_i = self.get_similarity_ratio(self.image_h, self.image_numbers[i])
                if image_similarity_i >= LOW_SIMILARITY_THRESHOLD and \
                        abs(image_similarity_g_h - image_similarity_i) <= 0.0001:
                    print 'Solving with Similar Image.'
                    # compare with all options ?
                    return i

        return -1

    def solve_triangular_image_pattern_3x3(self):
        image_multiply_b_d = ImageChops.multiply(self.image_b, self.image_d)
        image_diff_e_bd = self.get_similarity_ratio(image_multiply_b_d, self.image_e)
        if image_diff_e_bd > HIGH_SIMILARITY_THRESHOLD:
            image_multiply_c_g = ImageChops.multiply(self.image_c, self.image_g)
            for i in range(1, 9):
                image_diff_i_cg = self.get_similarity_ratio(image_multiply_c_g, self.image_numbers[i])
                if image_diff_i_cg > HIGH_SIMILARITY_THRESHOLD:
                    # compare with all options ?
                    print 'Triangular image pattern..'
                    return i
        return -1

    def solve_flip_image_pattern_3x3(self):
        image_at = self.image_a.transpose(Image.FLIP_LEFT_RIGHT)
        image_similarity_at_c = self.get_similarity_ratio(image_at, self.image_c)
        image_dt = self.image_d.transpose(Image.FLIP_LEFT_RIGHT)
        image_similarity_dt_f = self.get_similarity_ratio(image_dt, self.image_f)
        if image_similarity_at_c > HIGH_SIMILARITY_THRESHOLD and \
                image_similarity_dt_f > HIGH_SIMILARITY_THRESHOLD:
            image_gt = self.image_g.transpose(Image.FLIP_LEFT_RIGHT)
            for i in range(1, 9):
                image_similarity_gt_i = self.get_similarity_ratio(image_gt, self.image_numbers[i])
                if image_similarity_gt_i > HIGH_SIMILARITY_THRESHOLD:
                    # compare with all options ?
                    print 'Flip image pattern'
                    return i
        return -1

    # def solve_dark_pixel_ratio_3x3(self):
    #     print 'a', self.get_dark_pixel_ratio(self.image_a)
    #     print 'b', self.get_dark_pixel_ratio(self.image_b)
    #     print 'c', self.get_dark_pixel_ratio(self.image_c)
    #     print 'd', self.get_dark_pixel_ratio(self.image_d)
    #     print 'e', self.get_dark_pixel_ratio(self.image_e)
    #     print 'f', self.get_dark_pixel_ratio(self.image_f)
    #     print 'g', self.get_dark_pixel_ratio(self.image_g)
    #     print 'h', self.get_dark_pixel_ratio(self.image_h)
    #
    #     dpr_a = self.get_dark_pixel_ratio(self.image_a)
    #     dpr_b = self.get_dark_pixel_ratio(self.image_b)
    #     dpr_c = self.get_dark_pixel_ratio(self.image_c)
    #     dpr_d = self.get_dark_pixel_ratio(self.image_d)
    #     dpr_e = self.get_dark_pixel_ratio(self.image_e)
    #     dpr_f = self.get_dark_pixel_ratio(self.image_f)
    #     dpr_g = self.get_dark_pixel_ratio(self.image_g)
    #     dpr_h = self.get_dark_pixel_ratio(self.image_h)
    #
    #     print '### ', abs(dpr_a - dpr_b), ' ', abs(dpr_b - dpr_c), ' ', abs(dpr_d - dpr_e), ' ', abs(dpr_e - dpr_f)
    #
    #     if self.is_same(abs(dpr_a - dpr_b), abs(dpr_b - dpr_c), 0.003) \
    #             and self.is_same(abs(dpr_d - dpr_e), abs(dpr_e - dpr_f), 0.003):
    #         diff_g_h = dpr_g - dpr_h
    #         for i in range(1, 9):
    #             dpr_i = self.get_dark_pixel_ratio(self.image_numbers[i])
    #             expected_dpr_i = dpr_h - diff_g_h
    #             print dpr_i, ' --- ', expected_dpr_i
    #             if self.is_same(dpr_i, expected_dpr_i, 0.003):
    #                 return i
    #
    #     # for i in range(1, 9):
    #     #     print i, '-', self.get_dark_pixel_ratio(self.image_numbers[i])
    #
    #     return -1

    def solve_image_difference_3x3(self):
        diff_image_a_b = self.get_similarity_ratio(self.image_a, self.image_b)
        diff_image_b_c = self.get_similarity_ratio(self.image_b, self.image_c)
        diff_image_d_e = self.get_similarity_ratio(self.image_d, self.image_e)
        diff_image_e_f = self.get_similarity_ratio(self.image_e, self.image_f)
        diff_image_g_h = self.get_similarity_ratio(self.image_g, self.image_h)

        diff_row_1 = diff_image_a_b - diff_image_b_c
        diff_row_2 = diff_image_d_e - diff_image_e_f

        if round(diff_row_1 / diff_row_2, 2) == 1:
            print 'inside diff of 1'
            option = 0
            min_difference = 1
            for i in range(1, 9):
                diff_image_h_i = self.get_similarity_ratio(self.image_h, self.image_numbers[i])
                diff_row_3 = diff_image_g_h - diff_image_h_i
                difference = abs(round(diff_row_2 / diff_row_3, 2))
                # print i, diff_row_3, difference, 1 - difference
                if abs(1 - difference) < min_difference:
                    option = i
                    min_difference = abs(1 - difference)
            if option > 0 and min_difference < 0.1:
                # print "1*****", min_difference
                return option

        diff_row_1_2 = diff_row_1 - diff_row_2
        expected_diff_row_3 = diff_row_2 - diff_row_1_2

        # print "diff_row_1:", diff_row_1, " diff_row_2:", diff_row_2
        # print "diff_row_1_2:", diff_row_1_2, "expected_diff_row_3:", expected_diff_row_3

        diff_1 = abs(abs(diff_row_1) - abs(diff_row_1_2))
        diff_2 = abs(abs(diff_row_2) - abs(diff_row_1_2))

        if diff_1 < 0.00075 or diff_2 < 0.00075:
            print 'inside diff of 2'
            option = 0
            min_difference = 1
            for i in range(1, 9):
                diff_image_h_i = self.get_similarity_ratio(self.image_h, self.image_numbers[i])
                diff_row_3 = diff_image_g_h - diff_image_h_i
                difference = expected_diff_row_3 - diff_row_3
                # print i, expected_diff_row_3, diff_row_3, difference
                if 0 < difference < min_difference:
                    option = i
                    min_difference = difference
            if option > 0 and min_difference < 0.01:
                # print "2*****", min_difference
                return option

        return -1

    # 2x2 functions starts from here

    def solve_image_difference(self):
        # check for difference between image a and b, then find answer that has similar transition with c
        diff_image = ImageChops.invert(ImageChops.difference(self.image_a, self.image_b))
        new_image = ImageChops.invert(ImageChops.difference(self.image_c, diff_image))
        option = 0
        max_similarity_ratio = 0
        for i in range(1, 7):
            similarity_ratio = self.get_similarity_ratio(new_image, self.image_numbers[i])
            if round(similarity_ratio, 2) >= LOW_SIMILARITY_THRESHOLD and similarity_ratio > max_similarity_ratio:
                option = i
                max_similarity_ratio = similarity_ratio
        if option > 0:
            return option

        # check for difference between image a and c, then find answer that has similar transition with b
        diff_image = ImageChops.invert(ImageChops.difference(self.image_a, self.image_c))
        new_image = ImageChops.invert(ImageChops.difference(self.image_b, diff_image))
        option = 0
        max_similarity_ratio = 0
        for i in range(1, 7):
            similarity_ratio = self.get_similarity_ratio(new_image, self.image_numbers[i])
            if round(similarity_ratio, 2) >= LOW_SIMILARITY_THRESHOLD and similarity_ratio > max_similarity_ratio:
                option = i
                max_similarity_ratio = similarity_ratio
        if option > 0:
            return option

        return -1

    def solve_image_reflection(self):
        # left-right flip of image A is same as B, then find answer that has similar transition with C
        image_at = self.image_a.transpose(Image.FLIP_LEFT_RIGHT)
        image_ct = self.image_c.transpose(Image.FLIP_LEFT_RIGHT)
        index = 0
        curr_max_val = 0
        if self.get_similarity_ratio(image_at, self.image_b) > HIGH_SIMILARITY_THRESHOLD:
            for i in range(1, 7):
                similarity_ratio_ct_numbers = self.get_similarity_ratio(image_ct, self.image_numbers[i])
                if similarity_ratio_ct_numbers > LOW_SIMILARITY_THRESHOLD and similarity_ratio_ct_numbers > curr_max_val:
                    index = i
                    curr_max_val = similarity_ratio_ct_numbers
            if index > 0:
                return index

        # top-down flip of image A is same as C, then find answer that has similar transition with B
        image_at = self.image_a.transpose(Image.FLIP_TOP_BOTTOM)
        image_bt = self.image_b.transpose(Image.FLIP_TOP_BOTTOM)
        index = 0
        curr_max_value = 0
        if self.get_similarity_ratio(image_at, self.image_c) > HIGH_SIMILARITY_THRESHOLD:
            for i in range(1, 7):
                similarity_ratio_bt_numbers = self.get_similarity_ratio(image_bt, self.image_numbers[i])
                if similarity_ratio_bt_numbers > LOW_SIMILARITY_THRESHOLD and similarity_ratio_bt_numbers > curr_max_value:
                    index = i
                    curr_max_value = similarity_ratio_bt_numbers
            if index > 0:
                return index

        return -1

    def solve_image_rotation(self):
        # Rotate A from 90 to 270 and check if it is similar to C or B
        for k in range(1, 4):
            image_ar = self.image_a.convert('L').point(lambda i: i < 128 and 255).rotate(90 * k)
            image_br = self.image_b.convert('L').point(lambda i: i < 128 and 255).rotate(90 * k)
            image_cr = self.image_c.convert('L').point(lambda i: i < 128 and 255).rotate(90 * k)

            similarity_ratio_ar_c = self.get_similarity_ratio(image_ar, self.image_c.convert('L').point(
                lambda i: i < 128 and 255))
            similarity_ratio_ar_b = self.get_similarity_ratio(image_ar, self.image_b.convert('L').point(
                lambda i: i < 128 and 255))
            index = 0
            max_ratio = 0
            if round(similarity_ratio_ar_c, 2) >= LOW_SIMILARITY_THRESHOLD:
                for i in range(1, 7):
                    image_number = self.image_numbers[i].convert('L').point(lambda i: i < 128 and 255)
                    similarity_ratio_br_numbers = self.get_similarity_ratio(image_br, image_number)
                    if round(similarity_ratio_br_numbers,
                             2) >= LOW_SIMILARITY_THRESHOLD and similarity_ratio_br_numbers > max_ratio:
                        index = i
                        max_ratio = similarity_ratio_br_numbers
                if index > 0:
                    return index
            elif round(similarity_ratio_ar_b, 2) >= LOW_SIMILARITY_THRESHOLD:
                for i in range(1, 7):
                    image_number = self.image_numbers[i].convert('L').point(lambda i: i < 128 and 255)
                    similarity_ratio_cr_numbers = self.get_similarity_ratio(image_cr, image_number)
                    if round(similarity_ratio_cr_numbers,
                             2) >= LOW_SIMILARITY_THRESHOLD and similarity_ratio_cr_numbers > max_ratio:
                        index = i
                        max_ratio = similarity_ratio_cr_numbers
                if index > 0:
                    return index
        return -1

    def solve_image_fill(self):
        # Check if images a and b are unfilled/filled, then find answer that has similar transition with c
        new_image_a = self.fill_image(self.image_a)
        similarity_ratio_a_b = self.get_similarity_ratio(new_image_a, self.image_b)
        if round(similarity_ratio_a_b, 2) >= LOW_SIMILARITY_THRESHOLD:
            option = 0
            max_similarity_ratio = 0
            for i in range(1, 7):
                new_image_c = self.fill_image(self.image_c)
                similarity_ratio = self.get_similarity_ratio(new_image_c, self.image_numbers[i])
                if round(similarity_ratio, 2) >= LOW_SIMILARITY_THRESHOLD and similarity_ratio > max_similarity_ratio:
                    option = i
                    max_similarity_ratio = similarity_ratio
            if option > 0:
                return option
        return -1

    def solve_image_vertices_count(self):
        # count number of vertices for image a and b, apply same transition for c
        a_vertices = self.get_number_of_vertices(self.image_a)
        b_vertices = self.get_number_of_vertices(self.image_b)
        c_vertices = self.get_number_of_vertices(self.image_c)
        if a_vertices > b_vertices:
            diff_vertices_a_b = a_vertices - b_vertices
            dif_vertices_c_ab = c_vertices - diff_vertices_a_b
            for i in range(1, 7):
                if dif_vertices_c_ab == self.get_number_of_vertices(self.image_numbers[i]):
                    return i
        elif b_vertices > a_vertices:
            diff_vertices_a_b = b_vertices - a_vertices
            dif_vertices_c_ab = c_vertices + diff_vertices_a_b
            for i in range(1, 7):
                if dif_vertices_c_ab == self.get_number_of_vertices(self.image_numbers[i]):
                    return i

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

    def get_number_of_vertices(self, image):
        w, h = image.size
        D = image.getdata()
        B = {i % w + i / w * 1j for i in range(w * h) if D[i] != D[0]}
        n = d = 1
        o = v = q = p = max(B, key=abs)
        while p - w:
            p += d * 1j
            e = 2 * ({p} < B) + ({p + d} < B)
            if e != 2:
                e %= 2
                d *= 1j - e * 2j
                p -= d / 1j ** e
            if abs(p - q) > 5:
                t = (q - v) * (p - q).conjugate()
                q = p;
                w = o
                if .98 * abs(t) > t.real: n += 1; v = p
        return n

    def get_x_and_y_values_images(self, image):
        image_l = image.convert('L')
        img_binary = np.array(image_l)

        x_min = y_min = 200
        x_max = y_max = 0

        image_flag = False
        non_zero_count = image.width

        for x in range(img_binary.shape[0]):
            if image_flag is False and non_zero_count > np.count_nonzero(img_binary[x]):
                x_min = x
                image_flag = True
            if image_flag is True and non_zero_count == np.count_nonzero(img_binary[x]):
                x_max = x
                break

        image_flag = False
        non_zero_count = image.height

        for y in range(img_binary.shape[1]):
            if image_flag is False and non_zero_count > np.count_nonzero(img_binary[:, y]):
                y_min = y
                image_flag = True
            if image_flag is True and non_zero_count == np.count_nonzero(img_binary[:, y]):
                y_max = y
                break

        # for y in range(img_binary.shape[1]):
        #     if len(np.where(img_binary[:, y] == 0)[0]) > 0:
        #         if image_flag is False:
        #             y_min = np.where(img_binary[:, y] == 0)[0][0]
        #             image_flag = True
        #         if image_flag is True:
        #             y_max = np.where(img_binary[:, y] == 0)[0][0]
        #     if image_flag is True and non_zero_count == np.count_nonzero(img_binary[:, y]):
        #         break

        # print 'X:', x_min, x_max
        # print 'Y:', y_min, y_max
        return x_min, x_max, y_min, y_max

    def is_same(self, value1, value2, diff=0):
        return abs(value1 - value2) <= diff

    def get_dark_pixel_ratio(self, image):
        image_l = image.convert('L')
        img_binary = np.array(image_l)
        img_binary[img_binary < 50] = 1
        img_binary[img_binary >= 50] = 0
        black = 0
        for row in img_binary:
            for cell in row:
                if cell == 0:
                    black += 1
        return 1 - (black/float(image.height * image.width))
