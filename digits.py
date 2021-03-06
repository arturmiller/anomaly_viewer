import os

from sklearn.datasets import load_digits
import pandas as pd
import matplotlib.pylab as plt


if __name__ == '__main__':
    sk_digits = load_digits()
    feature_names = ['pixel_{}_{}'.format(feature_index//8, feature_index%8) for feature_index in range(sk_digits.data.shape[1])]
    pd_data = pd.DataFrame(data=sk_digits.data, columns=feature_names)

    curdir = os.path.dirname(os.path.abspath(__file__))
    url = ['file://' + os.path.join(curdir, 'digits/{}.png'.format(index)) for index in range(len(sk_digits.images))]
    pd_data['url'] = url
    pd_data.to_csv('digits.csv', index=False)

    if not os.path.exists('digits'):
        os.mkdir('digits')
    for (index, image) in enumerate(sk_digits.images):

        plt.imsave(os.path.join('digits', str(index) + '.png'), image, cmap='Greys_r')
