import cv2


class SteganoGraphy:

    def _init_(self):
        self.image_array = None

    def embed_data(self, data, key, start_row=1, start_col=1):

        self.image_array = cv2.imread("ant.png")

        data_len = len(data)
        key_len = len(key)

        data_index = 0
        key_index = 0

        row = start_row
        col = start_col

        # res = ""

        while row < self.image_array.shape[0] and data_index < data_len:

            while col < self.image_array.shape[1] and data_index < data_len:
                encrypted_char_ascii = ord(data[data_index]) ^ ord(key[key_index])

                # temp = encrypted_char_ascii ^ ord(key[key_index])
                # print(self.image_array[row, col], encrypted_char_ascii, chr(temp), end=" ")

                # splitted_bits [01  234  567] [B G R]
                splitted_bits = self.split_byte(encrypted_char_ascii)

                # print(data[data_index], ord(data[data_index]), encrypted_char_ascii, splitted_bits, row, col)
                # print(self.image_array[row, col])

                # free the bits
                self.image_array[row, col, 0] = self.image_array[row, col, 0] & 252
                self.image_array[row, col, 1] = self.image_array[row, col, 1] & 248
                self.image_array[row, col, 2] = self.image_array[row, col, 2] & 248

                # embed the bits
                self.image_array[row, col, 0] = self.image_array[row, col, 0] | splitted_bits[0]
                self.image_array[row, col, 1] = self.image_array[row, col, 1] | splitted_bits[1]
                self.image_array[row, col, 2] = self.image_array[row, col, 2] | splitted_bits[2]

                data_index = data_index + 1
                key_index = (key_index + 1) % key_len
                col = col + 1

            col = 0
            row = row + 1

        # print(res)

        cv2.imwrite("ant.png", self.image_array)

    def extract_data(self, key, qty_to_read, start_row=1, start_col=1):

        self.image_array = cv2.imread("ant.png")

        data_len = qty_to_read
        key_len = len(key)

        data_index = 0
        key_index = 0

        row = start_row
        col = start_col

        res = ""

        while row < self.image_array.shape[0] and data_index < data_len:

            while col < self.image_array.shape[1] and data_index < data_len:
                # extract bits
                b = self.image_array[row, col, 0] & 3
                g = self.image_array[row, col, 1] & 7
                r = self.image_array[row, col, 2] & 7

                # merge bits
                temp = b | (g << 2) | (r << 5)

                # decrypt
                temp = temp ^ ord(key[key_index])
                res = res + chr(temp)

                data_index = data_index + 1
                key_index = (key_index + 1) % key_len
                col = col + 1

            col = 0
            row = row + 1

            return res

    def split_byte(self, byte):
        last_two_bits = byte & 3
        mid_three_bits = (byte >> 2) & 7
        first_three_bits = byte >> 5
        return last_two_bits, mid_three_bits, first_three_bits


def main():
    em = SteganoGraphy()

    data = "anshuman moryaasdfff"
    key = "3456"



    #em.embed_data(data, key)

    tmp = em.extract_data(key, 20)
    print(tmp)


if __name__ == '__main__':
    main()
    
    
     