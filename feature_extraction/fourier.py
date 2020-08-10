import pandas as pd
import numpy as np

def get_denoise_fourier_transform(df, n_components, label='returns'):

    '''
    Calculate fourier transform, select the n_components most relevant components and then calculate the inverse fourier transform.
    '''
    
    returns_fourier = np.fft.fft(np.asarray(df[label].tolist()))

    fft_df = pd.DataFrame({'fft': returns_fourier})

    fft_df['absolute'] = fft_df['fft'].apply(lambda x: np.abs(x))

    fft_df['angle'] = fft_df['fft'].apply(lambda x: np.angle(x))

    fft_list = np.asarray(fft_df['fft'].tolist())

    fft_list_m10 = np.copy(fft_list)

    fft_list_m10[n_components:-n_components]=0

    df['n:'+str(n_components)+'-fourier'] = np.fft.ifft(fft_list_m10)                                                                    

    return df
