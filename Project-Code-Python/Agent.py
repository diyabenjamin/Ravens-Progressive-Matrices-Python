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
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

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
            option = self.solve_similar_xy_axes_image_3x3() if option == -1 else option
            option = self.solve_flip_image_pattern_3x3() if option == -1 else option
            option = self.solve_triangular_image_pattern_3x3() if option == -1 else option  # P2 D-11
            option = self.solve_row_combine_image_pattern_3x3() if option == -1 else option  # P3 E-01,02,03,06
            option = self.solve_extreme_triangular_image_similarity_3x3() if option == -1 else option  # P3 D-02,03

            option = self.solve_row_pixel_difference_3x3() if option == -1 else option  # P3 D-01, C-02,03

            option = self.solve_row_difference_images_3x3() if option == -1 else option  # P3 E-05,07,08
            option = self.solve_row_column_commonalities_3x3() if option == -1 else option  # P3 D-04,05
            option = self.solve_row_col_image_rotation_3x3() if option == -1 else option  # Challenge D-02,03
            option = self.solve_offset_images_3x3() if option == -1 else option

            option = self.solve_row_offset_difference_3x3() if option == -1 else option  # P3 E-04
            option = self.solve_row_dpr_subtract_3x3() if option == -1 else option  # P3 E-12

            option = self.split_image_horizontal_similarity_3x3() if option == -1 else option  # P3 E-09
            option = self.solve_extreme_triangular_multiply_3x3() if option == -1 else option  # P3 D-09
            option = self.solve_row_add_images_3x3() if option == -1 else option  # P3 E-10,11

            option = self.solve_dark_pixel_ratio_3x3() if option == -1 else option  # C-08

            option = self.solve_diagonal_subtract_mod_3x3() if option == -1 else option  # P3 D-06
            option = self.solve_extreme_triangular_dark_pixel_addition_3x3() if option == -1 else option  # P3 D-08
            # option = self.solve_diagonal_extreme_triangular_commonalities_3x3() if option == -1 else option  # P3 D-07

            option = self.solve_extreme_triangular_pixel_difference_3x3() if option == -1 else option  # P3 D-07,12
            option = self.solve_diagonal_commonalities_3x3() if option == -1 else option  # P3 3 D-10
            # option = self.solve_diagonal_difference_images_3x3() if option == -1 else option  # E-12
            return option

    # 3x3 functions starts from here

    def solve_row_dpr_subtract_3x3(self):
        diff_dpr_ab = self.get_dark_pixel_ratio(self.image_a) - self.get_dark_pixel_ratio(self.image_b)
        diff_dpr_de = self.get_dark_pixel_ratio(self.image_d) - self.get_dark_pixel_ratio(self.image_e)
        diff_dpr_gh = self.get_dark_pixel_ratio(self.image_g) - self.get_dark_pixel_ratio(self.image_h)
        if self.is_same(diff_dpr_ab, self.get_dark_pixel_ratio(self.image_c), 0.002) and \
                self.is_same(diff_dpr_de, self.get_dark_pixel_ratio(self.image_f), 0.002):
            for i in range(1, 9):
                if(self.is_same(diff_dpr_gh, self.get_dark_pixel_ratio(self.image_numbers[i]), 0.002)):
                    print 'row dpr subtract'
                    return i

        return -1

    def solve_row_pixel_difference_3x3(self):
        diff_dpr_ab = self.get_dark_pixel_ratio(self.image_a) - self.get_dark_pixel_ratio(self.image_b)
        diff_dpr_bc = self.get_dark_pixel_ratio(self.image_b) - self.get_dark_pixel_ratio(self.image_c)
        diff_dpr_de = self.get_dark_pixel_ratio(self.image_d) - self.get_dark_pixel_ratio(self.image_e)
        diff_dpr_ef = self.get_dark_pixel_ratio(self.image_e) - self.get_dark_pixel_ratio(self.image_f)
        diff_dpr_gh = self.get_dark_pixel_ratio(self.image_g) - self.get_dark_pixel_ratio(self.image_h)
        if self.is_same(diff_dpr_ab, diff_dpr_bc, 0.003) and self.is_same(diff_dpr_de, diff_dpr_ef, 0.003):
            for i in range(1, 9):
                diff_dpr_hi = self.get_dark_pixel_ratio(self.image_h) - self.get_dark_pixel_ratio(self.image_numbers[i])
                if self.is_same(diff_dpr_gh, diff_dpr_hi, 0.003):
                    print 'row image pixel difference'
                    return i
        return -1

    def solve_row_col_image_rotation_3x3(self):
        a = [45, 90, 180, 270, 315]
        for k in range(0, len(a)):
            # row rotations
            image_ar = self.image_a.convert('L').point(lambda i: i < 128 and 255).rotate(a[k])
            image_br = self.image_b.convert('L').point(lambda i: i < 128 and 255).rotate(a[k])
            image_gr = self.image_g.convert('L').point(lambda i: i < 128 and 255).rotate(a[k])
            image_hr = self.image_h.convert('L').point(lambda i: i < 128 and 255).rotate(a[k])
            index = 0
            max_ratio = 0
            if self.get_similarity_ratio(image_ar, self.image_b.convert('L').point(lambda i: i < 128 and 255)) > HIGH_SIMILARITY_THRESHOLD and \
                    self.get_similarity_ratio(image_br, self.image_c.convert('L').point(lambda i: i < 128 and 255)) > HIGH_SIMILARITY_THRESHOLD and \
                    self.get_similarity_ratio(image_gr, self.image_h.convert('L').point(lambda i: i < 128 and 255)) > HIGH_SIMILARITY_THRESHOLD:
                for i in range(1, 9):
                    similarity_br_i = self.get_similarity_ratio(image_hr, self.image_numbers[i].convert('L').point(lambda i: i < 128 and 255))
                    if similarity_br_i > HIGH_SIMILARITY_THRESHOLD and similarity_br_i > max_ratio:
                        index = i
                        max_ratio = similarity_br_i
                if index > 0:
                    print 'row image rotations..'
                    return index

            # column rotations
            image_cr = self.image_c.convert('L').point(lambda i: i < 128 and 255).rotate(a[k])
            image_dr = self.image_d.convert('L').point(lambda i: i < 128 and 255).rotate(a[k])
            image_fr = self.image_f.convert('L').point(lambda i: i < 128 and 255).rotate(a[k])
            if self.get_similarity_ratio(image_ar, self.image_d.convert('L').point(lambda i: i < 128 and 255)) > HIGH_SIMILARITY_THRESHOLD and \
                    self.get_similarity_ratio(image_dr, self.image_g.convert('L').point(lambda i: i < 128 and 255)) > HIGH_SIMILARITY_THRESHOLD and \
                    self.get_similarity_ratio(image_cr, self.image_f.convert('L').point(lambda i: i < 128 and 255)) > HIGH_SIMILARITY_THRESHOLD:
                for i in range(1, 9):
                    similarity_fr_i = self.get_similarity_ratio(image_fr, self.image_numbers[i].convert('L').point(lambda i: i < 128 and 255))
                    if similarity_fr_i > HIGH_SIMILARITY_THRESHOLD and similarity_fr_i > max_ratio:
                        index = i
                        max_ratio = similarity_fr_i
                if index > 0:
                    print 'column image rotations'
                    return index
        return -1

    def solve_extreme_triangular_dark_pixel_addition_3x3(self):
        diff_dpr_f_h = abs(self.get_dark_pixel_ratio(self.image_f) - self.get_dark_pixel_ratio(self.image_h))
        diff_dpr_b_d = abs(self.get_dark_pixel_ratio(self.image_b) - self.get_dark_pixel_ratio(self.image_d))
        if self.is_same(diff_dpr_f_h, self.get_dark_pixel_ratio(self.image_a), 0.02):
            for i in range(1, 9):
                if self.is_same(diff_dpr_b_d, self.get_dark_pixel_ratio(self.image_numbers[i]), 0.01):
                    print 'extreme triangular dpr addition..'
                    return i
        diff_dpr_b_f = abs(self.get_dark_pixel_ratio(self.image_b) - self.get_dark_pixel_ratio(self.image_f))
        diff_dpr_d_h = abs(self.get_dark_pixel_ratio(self.image_d) - self.get_dark_pixel_ratio(self.image_h))
        diff_dpr_a_e = abs(self.get_dark_pixel_ratio(self.image_a) - self.get_dark_pixel_ratio(self.image_e))
        if self.is_same(diff_dpr_b_f, self.get_dark_pixel_ratio(self.image_g), 0.02) and \
                self.is_same(diff_dpr_d_h, self.get_dark_pixel_ratio(self.image_c), 0.02):
            for i in range(1, 9):
                if self.is_same(diff_dpr_a_e, self.get_dark_pixel_ratio(self.image_numbers[i]), 0.01):
                    print 'extreme triangular dpr addition 2..'
                    return i
        return -1

    def solve_diagonal_commonalities_3x3(self):
        image_cd_add = ImageChops.add(self.image_c, self.image_d)
        image_dh_add = ImageChops.add(self.image_d, self.image_h)
        image_gb_add = ImageChops.add(self.image_g, self.image_b)
        image_bf_add = ImageChops.add(self.image_b, self.image_f)
        image_ae_add = ImageChops.add(self.image_a, self.image_e)
        if self.get_similarity_ratio(image_cd_add, image_dh_add) > HIGH_SIMILARITY_THRESHOLD and \
                self.get_similarity_ratio(image_gb_add, image_bf_add) > HIGH_SIMILARITY_THRESHOLD:
            for i in range(1, 9):
                image_ei_add = ImageChops.add(self.image_e, self.image_numbers[i])
                if self.get_similarity_ratio(image_ae_add, image_ei_add) > LOW_SIMILARITY_THRESHOLD and \
                    self.is_same(self.get_dark_pixel_ratio(image_ae_add), self.get_dark_pixel_ratio(image_ei_add), 0.03) and \
                        not self.get_similarity_ratio(self.image_a, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_e, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD:
                    print 'diagonal commonalities images..'
                    return i

        image_ce_add = ImageChops.add(self.image_c, self.image_e)
        image_eg_add = ImageChops.add(self.image_e, self.image_g)
        image_ah_add = ImageChops.add(self.image_a, self.image_h)
        image_hf_add = ImageChops.add(self.image_h, self.image_f)
        image_bd_add = ImageChops.add(self.image_b, self.image_d)
        if self.get_similarity_ratio(image_ce_add, image_eg_add) > HIGH_SIMILARITY_THRESHOLD and \
                self.get_similarity_ratio(image_ah_add, image_hf_add) > HIGH_SIMILARITY_THRESHOLD:
            for i in range(1, 9):
                image_bi_add = ImageChops.add(self.image_b, self.image_numbers[i])
                image_di_add = ImageChops.add(self.image_d, self.image_numbers[i])
                if self.is_same(self.get_dark_pixel_ratio(image_bd_add), self.get_dark_pixel_ratio(image_bi_add), 0.01) and \
                        self.is_same(self.get_dark_pixel_ratio(image_bd_add), self.get_dark_pixel_ratio(image_di_add), 0.01) and \
                        self.get_similarity_ratio(image_bd_add, image_bi_add) > LOW_SIMILARITY_THRESHOLD and \
                        self.get_similarity_ratio(image_bd_add, image_di_add) > LOW_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_a, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_b, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_c, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_d, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_e, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_f, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_g, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD and \
                        not self.get_similarity_ratio(self.image_h, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD:
                    print 'diagonal commonalities images 2..'
                    return i
        return -1

    def split_image_horizontal_similarity_3x3(self):
        upper_border = (0, 0, 0, 92)  # upper half
        lower_border = (0, 92, 0, 0)  # lower half
        image_a_upper = ImageOps.crop(self.image_a, upper_border)
        image_a_lower = ImageOps.crop(self.image_a, lower_border)
        image_b_upper = ImageOps.crop(self.image_b, upper_border)
        image_b_lower = ImageOps.crop(self.image_b, lower_border)
        image_c_upper = ImageOps.crop(self.image_c, upper_border)
        image_c_lower = ImageOps.crop(self.image_c, lower_border)
        image_g_upper = ImageOps.crop(self.image_g, upper_border)
        image_g_lower = ImageOps.crop(self.image_g, lower_border)
        image_h_upper = ImageOps.crop(self.image_h, upper_border)
        image_h_lower = ImageOps.crop(self.image_h, lower_border)

        if self.is_same(self.get_dark_pixel_ratio(image_a_upper), self.get_dark_pixel_ratio(image_c_upper), 0.001) and \
                self.is_same(self.get_dark_pixel_ratio(image_b_lower), self.get_dark_pixel_ratio(image_c_lower), 0.001):
            for i in range(1, 9):
                image_i_upper = ImageOps.crop(self.image_numbers[i], upper_border)
                image_i_lower = ImageOps.crop(self.image_numbers[i], lower_border)
                if self.is_same(self.get_dark_pixel_ratio(image_g_upper), self.get_dark_pixel_ratio(image_i_upper), 0.0001) and \
                        self.is_same(self.get_dark_pixel_ratio(image_h_lower), self.get_dark_pixel_ratio(image_i_lower), 0.0001):
                    print 'split image horizontal similarity'
                    return i

        if self.is_same(self.get_dark_pixel_ratio(image_b_upper), self.get_dark_pixel_ratio(image_c_upper), 0.0001) and \
                self.is_same(self.get_dark_pixel_ratio(image_a_lower), self.get_dark_pixel_ratio(image_c_lower), 0.0001):
            for i in range(1, 9):
                image_i_upper = ImageOps.crop(self.image_numbers[i], upper_border)
                image_i_lower = ImageOps.crop(self.image_numbers[i], lower_border)
                if self.is_same(self.get_dark_pixel_ratio(image_h_upper), self.get_dark_pixel_ratio(image_i_upper), 0.0001) and \
                        self.is_same(self.get_dark_pixel_ratio(image_g_lower), self.get_dark_pixel_ratio(image_i_lower), 0.0001):
                    print 'split image horizontal similarity 2'
                    return i
        return -1

    def solve_extreme_triangular_pixel_difference_3x3(self):
        dpr_diff_a_f = abs(self.get_dark_pixel_ratio(self.image_a) - self.get_dark_pixel_ratio(self.image_f))
        dpr_diff_f_h = abs(self.get_dark_pixel_ratio(self.image_f) - self.get_dark_pixel_ratio(self.image_h))
        if self.is_same(dpr_diff_a_f, dpr_diff_f_h, 0.006):
            dpr_diff_b_d = abs(self.get_dark_pixel_ratio(self.image_b) - self.get_dark_pixel_ratio(self.image_d))
            for i in range(1, 9):
                dpr_diff_b_i = abs(self.get_dark_pixel_ratio(self.image_b) - self.get_dark_pixel_ratio(self.image_numbers[i]))
                dpr_diff_d_i = abs(self.get_dark_pixel_ratio(self.image_d) - self.get_dark_pixel_ratio(self.image_numbers[i]))
                if self.is_same(dpr_diff_b_d, dpr_diff_b_i, 0.006) or self.is_same(dpr_diff_b_d, dpr_diff_d_i, 0.006):
                    print 'extreme triangular pixel diff'
                    return i

        dpr_diff_c_d = abs(self.get_dark_pixel_ratio(self.image_c) - self.get_dark_pixel_ratio(self.image_d))
        dpr_diff_d_h = abs(self.get_dark_pixel_ratio(self.image_d) - self.get_dark_pixel_ratio(self.image_h))
        if self.is_same(dpr_diff_c_d, dpr_diff_d_h, 0.006):
            dpr_diff_a_e = abs(self.get_dark_pixel_ratio(self.image_a) - self.get_dark_pixel_ratio(self.image_e))
            for i in range(1, 9):
                dpr_diff_a_i = abs(self.get_dark_pixel_ratio(self.image_a) - self.get_dark_pixel_ratio(self.image_numbers[i]))
                dpr_diff_e_i = abs(self.get_dark_pixel_ratio(self.image_e) - self.get_dark_pixel_ratio(self.image_numbers[i]))
                if self.is_same(dpr_diff_a_e, dpr_diff_a_i, 0.006) or self.is_same(dpr_diff_a_e, dpr_diff_e_i, 0.006):
                    print 'extreme triangular pixel diff 2'
                    return i
        return -1

    def solve_extreme_triangular_multiply_3x3(self):
        image_a_f = ImageChops.multiply(self.image_a, self.image_f)
        if self.is_same(self.get_dark_pixel_ratio(image_a_f), self.get_dark_pixel_ratio(self.image_h), 0.009) and \
                self.get_similarity_ratio(image_a_f, self.image_h) > HIGH_SIMILARITY_THRESHOLD:
            for i in range(1, 9):
                image_b_i = ImageChops.multiply(self.image_b, self.image_numbers[i])
                if self.is_same(self.get_dark_pixel_ratio(image_b_i), self.get_dark_pixel_ratio(self.image_d), 0.009) and \
                        self.get_similarity_ratio(image_b_i, self.image_d) > HIGH_SIMILARITY_THRESHOLD:
                    print 'row extreme triangular multiply images 1..'
                    return i

        image_a_h = ImageChops.multiply(self.image_a, self.image_h)
        if self.is_same(self.get_dark_pixel_ratio(image_a_h), self.get_dark_pixel_ratio(self.image_f), 0.009) and \
                self.get_similarity_ratio(image_a_h, self.image_f) > HIGH_SIMILARITY_THRESHOLD:
            for i in range(1, 9):
                image_d_i = ImageChops.multiply(self.image_d, self.image_numbers[i])
                if self.is_same(self.get_dark_pixel_ratio(image_d_i), self.get_dark_pixel_ratio(self.image_b), 0.009) and \
                        self.get_similarity_ratio(image_d_i, self.image_b) > HIGH_SIMILARITY_THRESHOLD:
                    print 'row extreme triangular multiply images 2..'
                    return i

        image_f_h = ImageChops.multiply(self.image_f, self.image_h)
        if self.is_same(self.get_dark_pixel_ratio(image_f_h), self.get_dark_pixel_ratio(self.image_a), 0.009) and \
                self.get_similarity_ratio(image_f_h, self.image_a) > HIGH_SIMILARITY_THRESHOLD:
            for i in range(1, 9):
                image_b_d = ImageChops.multiply(self.image_b, self.image_d)
                if self.is_same(self.get_dark_pixel_ratio(image_b_d), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.009) and \
                        self.get_similarity_ratio(image_b_d, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD:
                    print 'row extreme triangular multiply images 3..'
                    return i
        return -1

    def solve_row_column_commonalities_3x3(self):
        image_g_h = ImageChops.add(self.image_g, self.image_h)
        image_c_f = ImageChops.add(self.image_c, self.image_f)
        image_row_col = ImageChops.multiply(image_g_h, image_c_f)
        for i in range(1, 9):
            if self.is_same(self.get_dark_pixel_ratio(image_row_col), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.006) and \
                    self.get_similarity_ratio(image_row_col, self.image_numbers[i]) >= HIGH_SIMILARITY_THRESHOLD:
                print 'row column commonalities images..'
                return i

        image_g_h = ImageChops.invert(ImageChops.difference(self.image_g, self.image_h))
        image_c_f = ImageChops.invert(ImageChops.difference(self.image_c, self.image_f))
        image_row_col = ImageChops.multiply(image_g_h, image_c_f)
        for i in range(1, 9):
            if self.is_same(self.get_dark_pixel_ratio(image_row_col), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.009) and \
                    self.get_similarity_ratio(image_row_col, self.image_numbers[i]) >= HIGH_SIMILARITY_THRESHOLD:
                print 'row column commonalities images 2..'
                return i
        return -1

    # def solve_diagonal_extreme_triangular_commonalities_3x3(self):
    #     image_a_e = ImageChops.add(self.image_a, self.image_e)
    #     image_b_d = ImageChops.add(self.image_b, self.image_d)
    #     image_diag_triag = ImageChops.multiply(image_a_e, image_b_d)
    #     for i in range(1, 9):
    #         if self.is_same(self.get_dark_pixel_ratio(image_diag_triag), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.006):
    #             if self.get_similarity_ratio(image_diag_triag, self.image_numbers[i]) >= HIGH_SIMILARITY_THRESHOLD:
    #                 print 'diag triag commonalities images..'
    #                 return i
    #     return -1

    def solve_diagonal_subtract_mod_3x3(self):
        image_ae = ImageChops.subtract_modulo(self.image_a, self.image_e)
        for i in range(1, 9):
            image_ei = ImageChops.subtract_modulo(self.image_e, self.image_numbers[i])
            if self.is_same(self.get_dark_pixel_ratio(image_ae), self.get_dark_pixel_ratio(image_ei), 0.0006):
                if self.get_similarity_ratio(image_ae, image_ei) >= HIGH_SIMILARITY_THRESHOLD:
                    print 'diagonal subtract mod images..'
                    return i
        return -1

    def solve_row_offset_difference_3x3(self):
        image_b_o = ImageChops.offset(self.image_b, xoffset=-50, yoffset=0)
        image_a_bo = ImageChops.invert(ImageChops.difference(self.image_a, image_b_o))
        image_c_offset = ImageChops.offset(image_a_bo, xoffset=-26, yoffset=0)

        image_e_o = ImageChops.offset(self.image_e, xoffset=-50, yoffset=0)
        image_d_eo = ImageChops.invert(ImageChops.difference(self.image_d, image_e_o))
        image_f_offset = ImageChops.offset(image_d_eo, xoffset=-26, yoffset=0)

        image_h_o = ImageChops.offset(self.image_h, xoffset=-50, yoffset=0)
        image_g_ho = ImageChops.invert(ImageChops.difference(self.image_g, image_h_o))
        image_i_offset = ImageChops.offset(image_g_ho, xoffset=-26, yoffset=0)

        if self.get_similarity_ratio(image_c_offset, self.image_c) > HIGH_SIMILARITY_THRESHOLD and \
                self.get_similarity_ratio(image_f_offset, self.image_f) > HIGH_SIMILARITY_THRESHOLD:
            max_ratio = 0
            option = 0
            for i in range(1, 9):
                similarity_i = self.get_similarity_ratio(image_i_offset, self.image_numbers[i])
                if similarity_i > HIGH_SIMILARITY_THRESHOLD and similarity_i > max_ratio:
                    option = i
                    max_ratio = similarity_i
                    print 'Row offset difference images..'
            if option > 0:
                return option
        return -1

    def solve_row_combine_image_pattern_3x3(self):
        image_a_b = ImageChops.multiply(self.image_a, self.image_b)
        image_d_e = ImageChops.multiply(self.image_d, self.image_e)
        image_g_h = ImageChops.multiply(self.image_g, self.image_h)
        image_a_c = ImageChops.multiply(self.image_a, self.image_c)
        image_d_f = ImageChops.multiply(self.image_d, self.image_f)

        if self.is_same(self.get_dark_pixel_ratio(image_a_b), self.get_dark_pixel_ratio(self.image_c), 0.001) and \
                self.is_same(self.get_dark_pixel_ratio(image_d_e), self.get_dark_pixel_ratio(self.image_f), 0.001):
            for i in range(1, 9):
                if self.is_same(self.get_dark_pixel_ratio(image_g_h), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.002) and \
                        not self.is_same(self.get_dark_pixel_ratio(self.image_g), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.001) and \
                        not self.is_same(self.get_dark_pixel_ratio(self.image_h), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.001) and \
                        self.get_similarity_ratio(image_g_h, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD:
                    print 'Row combine images..'
                    return i
        elif self.is_same(self.get_dark_pixel_ratio(image_a_c), self.get_dark_pixel_ratio(self.image_b), 0.001) and \
                self.is_same(self.get_dark_pixel_ratio(image_d_f), self.get_dark_pixel_ratio(self.image_e), 0.001):
            for i in range(1, 9):
                image_g_i = ImageChops.multiply(self.image_g, self.image_numbers[i])
                if self.is_same(self.get_dark_pixel_ratio(image_g_i), self.get_dark_pixel_ratio(self.image_h), 0.0005) and \
                        not self.is_same(self.get_dark_pixel_ratio(self.image_h), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.001) and \
                        self.get_similarity_ratio(image_g_i, self.image_h) > HIGH_SIMILARITY_THRESHOLD:
                    print 'Row combine images 2..'
                    return i
        return -1

    def solve_row_add_images_3x3(self):
        image_a_b = ImageChops.add(self.image_a, self.image_b)
        image_d_e = ImageChops.add(self.image_d, self.image_e)
        image_g_h = ImageChops.add(self.image_g, self.image_h)
        if self.get_similarity_ratio(image_a_b, self.image_c) > HIGH_SIMILARITY_THRESHOLD and \
                self.get_similarity_ratio(image_d_e, self.image_f) > HIGH_SIMILARITY_THRESHOLD:
            max_ratio = 0
            option = 0
            for i in range(1, 9):
                similarity_gh_i = self.get_similarity_ratio(image_g_h, self.image_numbers[i])
                if similarity_gh_i > HIGH_SIMILARITY_THRESHOLD and similarity_gh_i > max_ratio:
                    option = i
                    max_ratio = similarity_gh_i
                    print 'Row add images..'
            if option > 0:
                return option
        return -1

    # def solve_row_difference_images_3x3(self):
    #     diff_ab = ImageChops.invert(ImageChops.difference(self.image_a, self.image_b))
    #     diff_de = ImageChops.invert(ImageChops.difference(self.image_d, self.image_e))
    #     diff_gh = ImageChops.invert(ImageChops.difference(self.image_g, self.image_h))
    #     print self.get_similarity_ratio(diff_ab, self.image_c), self.get_similarity_ratio(diff_de, self.image_f)
    #     if self.get_similarity_ratio(diff_ab, self.image_c) > HIGH_SIMILARITY_THRESHOLD and \
    #             self.get_similarity_ratio(diff_de, self.image_f) > HIGH_SIMILARITY_THRESHOLD:
    #         max_ratio = 0
    #         option = 0
    #         for i in range(1, 9):
    #             similarity_ratio_ghi = self.get_similarity_ratio(diff_gh, self.image_numbers[i])
    #             print 'i: ', i, similarity_ratio_ghi
    #             if similarity_ratio_ghi > HIGH_SIMILARITY_THRESHOLD and similarity_ratio_ghi > max_ratio:
    #                 option = i
    #                 max_ratio = similarity_ratio_ghi
    #                 print 'Row difference invert images..'
    #         if option > 0:
    #             return option
    #     return -1

    def solve_row_difference_images_3x3(self):
        diff_ab = ImageChops.invert(ImageChops.difference(self.image_a, self.image_b))
        diff_de = ImageChops.invert(ImageChops.difference(self.image_d, self.image_e))
        diff_gh = ImageChops.invert(ImageChops.difference(self.image_g, self.image_h))

        if self.get_similarity_ratio(diff_ab, self.image_c) > HIGH_SIMILARITY_THRESHOLD and \
                self.get_similarity_ratio(diff_de, self.image_f) > HIGH_SIMILARITY_THRESHOLD:
            for i in range(1, 9):
                if self.get_similarity_ratio(diff_gh, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD:
                    print 'Row difference images..'
                    return i

        diff_ab_c = ImageChops.multiply(diff_ab, self.image_c)
        diff_de_f = ImageChops.multiply(diff_de, self.image_f)
        if self.is_same(self.get_dark_pixel_ratio(diff_ab_c), self.get_dark_pixel_ratio(self.image_c), 0.01) and \
                self.is_same(self.get_dark_pixel_ratio(diff_de_f), self.get_dark_pixel_ratio(self.image_f), 0.02):
            for i in range(1, 9):
                diff_gh_i = ImageChops.multiply(diff_gh, self.image_numbers[i])
                if self.is_same(self.get_dark_pixel_ratio(diff_gh_i), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.01) and \
                        not self.is_same(self.get_dark_pixel_ratio(self.image_g), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.01) and \
                        not self.is_same(self.get_dark_pixel_ratio(self.image_h), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.01) and \
                        self.get_similarity_ratio(diff_gh_i, self.image_numbers[i]) > HIGH_SIMILARITY_THRESHOLD:
                    print 'Row difference images 2..'
                    return i
        return -1

    def solve_extreme_triangular_image_similarity_3x3(self):
        image_diff_c_d = self.get_similarity_ratio(self.image_c, self.image_d)
        image_diff_c_h = self.get_similarity_ratio(self.image_c, self.image_h)
        image_diff_g_b = self.get_similarity_ratio(self.image_g, self.image_b)
        image_diff_g_f = self.get_similarity_ratio(self.image_g, self.image_f)
        image_diff_a_e = self.get_similarity_ratio(self.image_a, self.image_e)
        if image_diff_c_d >= HIGH_SIMILARITY_THRESHOLD and image_diff_c_h >= HIGH_SIMILARITY_THRESHOLD and \
                image_diff_g_b >= HIGH_SIMILARITY_THRESHOLD and image_diff_g_f >= HIGH_SIMILARITY_THRESHOLD:
            if image_diff_a_e >= LOW_SIMILARITY_THRESHOLD:
                max_ratio = 0
                option = 0
                for i in range(1, 9):
                    image_diff_i_ei = self.get_similarity_ratio(self.image_e, self.image_numbers[i])
                    if image_diff_i_ei >= HIGH_SIMILARITY_THRESHOLD and image_diff_i_ei > max_ratio:
                        option = i
                        max_ratio = image_diff_i_ei
                        print 'Extreme triangular image similarity..'
                if option > 0:
                    return option
        return -1

    # def solve_diagonal_difference_images_3x3(self):
    #     # diagonal similarity
    #     # if self.get_dark_pixel_ratio(self.image_a) == self.get_dark_pixel_ratio(self.image_e):
    #     #     for i in range(1, 9):
    #     #         if self.get_dark_pixel_ratio(self.image_a) == self.get_dark_pixel_ratio(self.image_numbers[i]):
    #     #             print 'diagonal similarity'
    #     #             return i
    #     # else:
    #     # diagonal decrease
    #     diff_a_e = self.get_dark_pixel_ratio(self.image_a) - self.get_dark_pixel_ratio(self.image_e)
    #     for i in range(1, 9):
    #         diff_e_i = self.get_dark_pixel_ratio(self.image_e) - self.get_dark_pixel_ratio(self.image_numbers[i])
    #         if self.is_same(diff_a_e, diff_e_i, 0.003):
    #             print 'diagonal decrease'
    #             return i
    #     return -1

    def solve_offset_images_3x3(self):
        image_a_o = ImageChops.offset(self.image_a, xoffset=self.image_a.width/2, yoffset=0)
        image_d_o = ImageChops.offset(self.image_d, xoffset=self.image_d.width/2, yoffset=0)
        image_g_o = ImageChops.offset(self.image_g, xoffset=self.image_g.width/2, yoffset=0)
        if self.is_same(self.get_dark_pixel_ratio(image_a_o), self.get_dark_pixel_ratio(self.image_c), 0.0009) and \
                self.is_same(self.get_dark_pixel_ratio(image_d_o), self.get_dark_pixel_ratio(self.image_f), 0.0009):
            for i in range(1, 9):
                if self.is_same(self.get_dark_pixel_ratio(image_g_o), self.get_dark_pixel_ratio(self.image_numbers[i]), 0.0009):
                    print 'offset row images..'
                    return i
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

    def solve_triangular_image_pattern_3x3(self):
        image_multiply_b_d = ImageChops.multiply(self.image_b, self.image_d)
        image_diff_e_bd = self.get_similarity_ratio(image_multiply_b_d, self.image_e)
        if image_diff_e_bd > HIGH_SIMILARITY_THRESHOLD:
            image_multiply_c_g = ImageChops.multiply(self.image_c, self.image_g)
            max_ratio = 0
            option = 0
            for i in range(1, 9):
                image_diff_i_cg = self.get_similarity_ratio(image_multiply_c_g, self.image_numbers[i])
                if image_diff_i_cg > HIGH_SIMILARITY_THRESHOLD and image_diff_i_cg > max_ratio:
                    option = i
                    max_ratio = image_diff_i_cg
                    print 'Triangular image pattern..'
            if option > 0:
                return option
        return -1

    def solve_flip_image_pattern_3x3(self):
        image_at = self.image_a.transpose(Image.FLIP_LEFT_RIGHT)
        image_similarity_at_c = self.get_similarity_ratio(image_at, self.image_c)
        image_dt = self.image_d.transpose(Image.FLIP_LEFT_RIGHT)
        image_similarity_dt_f = self.get_similarity_ratio(image_dt, self.image_f)
        if image_similarity_at_c > HIGH_SIMILARITY_THRESHOLD and \
                image_similarity_dt_f > HIGH_SIMILARITY_THRESHOLD:
            image_gt = self.image_g.transpose(Image.FLIP_LEFT_RIGHT)
            max_ratio = 0
            option = 0
            for i in range(1, 9):
                image_similarity_gt_i = self.get_similarity_ratio(image_gt, self.image_numbers[i])
                if image_similarity_gt_i > HIGH_SIMILARITY_THRESHOLD and image_similarity_gt_i > max_ratio:
                    option = i
                    max_ratio = image_similarity_gt_i
                    print 'Flip image pattern'
            if option > 0:
                return option
        return -1

    def solve_dark_pixel_ratio_3x3(self):
        dpr_a = self.get_dark_pixel_ratio(self.image_a)
        dpr_b = self.get_dark_pixel_ratio(self.image_b)
        dpr_c = self.get_dark_pixel_ratio(self.image_c)
        dpr_d = self.get_dark_pixel_ratio(self.image_d)
        dpr_e = self.get_dark_pixel_ratio(self.image_e)
        dpr_f = self.get_dark_pixel_ratio(self.image_f)
        dpr_g = self.get_dark_pixel_ratio(self.image_g)
        dpr_h = self.get_dark_pixel_ratio(self.image_h)

        # row difference
        if self.is_same(abs(dpr_a - dpr_b), abs(dpr_b - dpr_c), 0.002) \
                and self.is_same(abs(dpr_d - dpr_e), abs(dpr_e - dpr_f), 0.002):
            diff_g_h = dpr_g - dpr_h
            option = 0
            min_diff = 0.1
            for i in range(1, 9):
                dpr_i = self.get_dark_pixel_ratio(self.image_numbers[i])
                expected_dpr_i = dpr_h - diff_g_h
                if self.is_same(dpr_i, expected_dpr_i, 0.002) and abs(dpr_i - expected_dpr_i) < min_diff:
                    min_diff = abs(dpr_i - expected_dpr_i)
                    option = i
            if option > 0:
                print 'Inside dpr1 - row increase'
                return option

        # column difference C-11
        if self.is_same(abs(dpr_a - dpr_d), abs(dpr_d - dpr_g), 0.002) \
                and self.is_same(abs(dpr_b - dpr_e), abs(dpr_e - dpr_h), 0.002):
            diff_c_f = dpr_c - dpr_f
            option = 0
            min_diff = 0.1
            for i in range(1, 9):
                dpr_i = self.get_dark_pixel_ratio(self.image_numbers[i])
                expected_dpr_i = dpr_f - diff_c_f
                if self.is_same(dpr_i, expected_dpr_i, 0.002) and abs(dpr_i - expected_dpr_i) < min_diff:
                    min_diff = abs(dpr_i - expected_dpr_i)
                    option = i
            if option > 0:
                print 'Inside dpr2 - column increase'
                return option

        diff_g_h = dpr_g - dpr_h
        if self.is_same(dpr_c - dpr_f, diff_g_h, 0.007):
            option = 0
            min_diff = 0.1
            for i in range(1, 9):
                dpr_i = self.get_dark_pixel_ratio(self.image_numbers[i])
                dpr_h_i = dpr_h - dpr_i
                if self.is_same(diff_g_h, dpr_h_i, 0.007) and abs(diff_g_h - dpr_h_i) < min_diff:
                    min_diff = abs(diff_g_h - dpr_h_i)
                    option = i
            if option > 0:
                print 'Inside dpr3'
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
