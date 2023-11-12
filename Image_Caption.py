import os
import pickle
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model

class Image_Caption:
    vgg_model = VGG16()
    vgg_model = Model(inputs=vgg_model.inputs, outputs=vgg_model.layers[-2].output)

    model = load_model('best_model.h5')

    with open('features.pkl', 'rb') as f:
        features = pickle.load(f)

    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)

    def image_from_base64(self, base64_str):
        # Chuyển đổi chuỗi base64 thành hình ảnh
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))

        # Chuyển đổi hình ảnh từ RGBA (4 kênh) thành RGB (3 kênh)
        image = image.convert('RGB')

        # Thay đổi kích thước hình ảnh về (224, 224)
        image = image.resize((224, 224))

        return image
    def model_run_base64(self, base64_str):
        # Chuyển đổi base64 thành hình ảnh
        image = self.image_from_base64(base64_str)

        # Tạo chú thích
        max_length = 35
        caption = self.generate_caption(image, max_length)
        return caption

    def generate_caption(self, image, max_length):
        # Thực hiện các bước tương tự với hình ảnh thay vì đường dẫn file
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        feature = self.vgg_model.predict(image, verbose=0)

        in_text = 'startseq'
        generated_caption = []

        for _ in range(max_length):
            sequence = self.tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], maxlen=max_length)
            yhat = self.model.predict([feature, sequence], verbose=0)
            yhat = np.argmax(yhat)
            word = self.idx_to_word(yhat)
            if word is None or word == 'endseq':
                break
            in_text += ' ' + word
            generated_caption.append(word)

        return {'generated_caption': ' '.join(generated_caption)}

    def idx_to_word(self, integer):
        for word, index in self.tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    def model_run(self, base64_str):
        print("Received base64 string:", base64_str)
        try:
            # Sử dụng hàm model_run_base64 để xử lý base64
            caption = self.model_run_base64(base64_str)
            return caption
        except Exception as e:
            print("Error:", str(e))
            return {'error': str(e)}
