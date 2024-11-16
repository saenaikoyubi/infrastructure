class Params:
    def __init__(self):
        
        # Train > GenerateTrainData
        self.cols1 = ['open', 'high', 'low', 'close', 'mean', 'VWMean', 'median', '25%', '50%', '75%','center']
        self.cols2 = ['buySideMean', 'sellSideMean', 'buySideVWMean', 'sellSideVWMean', 'buySideMedian', 'sellSideMedian', 'buySideCenter', 'sellSideCenter',\
            'buySide25%', 'buySide50%', 'buySide75%', 'sellSide25%', 'sellSide50%', 'sellSide75%']
        self.cols3 = ['sideMean', 'sideMedian', 'priceChangeMean']
        self.cols4 = ['opentime', 'closetime', 'time25%', 'time50%', 'time75%']
        self.cols5 = ['reHighPrice', 'reLowPrice', 'reClosePrice', 'reMeanPrice', 'reMedianPrice', 're25%Price', 're50%Price', 're75%Price','reCenterPrice', \
            'reHighCuSize', 'reLowCuSize', 'reCloseCuSize', 'reMeanCuSize', 'reMedianCuSize', 're25%CuSize', 're50%CuSize', 're75%CuSize','reCenterCuSize']
        