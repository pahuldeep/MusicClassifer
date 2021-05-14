def getmetadata(filename):
    import librosa
    import numpy as np
    import math
    
    signal, sample_rate = librosa.load(filename)

    TRACK_DURATION = 30 # measured in seconds
    SAMPLES_PER_TRACK = sample_rate * TRACK_DURATION
    
    num_segments = 10
    hop_length = 512
    
    samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    num_mfcc_per_segment = math.ceil(samples_per_segment / hop_length)
    
    data = {
        "mfcc": []
    } 
    # process all segments of audio file
    for d in range(num_segments):
        start = samples_per_segment * d
        finish = start + samples_per_segment

        # extract mfcc
        mfcc = librosa.feature.mfcc(signal[:finish], sample_rate)
        mfcc = mfcc.T

        # store only mfcc feature with expected number of vectors
        if len(mfcc) == num_mfcc_per_segment:
            data["mfcc"].append(mfcc.tolist())
    return np.array(list(data.values())).squeeze(0)
