import pandas as pd

def conta_segundos(instante, secs):
    
    from datetime import timedelta
    
    '''
    Essa função recebe um timestamp do pandas, faz uma alteração temporal nele e retorna um novo timestamp.
    Lembre-se que o Pandas trabalha apenas com o timestamp, então não é possível fazer as alterações temporais direto
    nos timestamps. Por esse motivo, essa função já faz a operação e conversão das estruturas de dados.
    Inputs
    instante: (timestamp) que será alterado. 
    secs: quantidade de segundos que será alterado (+ pra frente) (- pra trás)
    Output
    Tempo alterado como timestamp de acordo com input secs.
    '''
    
    instante = instante.to_pydatetime()
    
    tempo_futuro = instante + timedelta(seconds=secs)
    
    tempo_futuro = pd.Timestamp(tempo_futuro)
    
    return tempo_futuro


def purgeKfold(X, Y, purge, k, score_metric, scaler, model):

    if len(X) != len(Y):

        raise Exception("[ERROR] Lenghts of X and Y doesn't match!")
    
    '''

    Purge K Fold implementation

    Similar (but not the same) to  Advances in Financial Machine Learning

    Passe como argumento X e Y que tenham index datetime

    purge deve ser fornecido em segundos

    '''

    metrics = []

    for i in range(1, k+1):

    X['index_aux'] = range(0, X.shape[0])
    Y['index_aux'] = range(0, Y.shape[0])

    print("[INFO] Iteration: "+str(i))

        if i == 1:

            X_test = X[(X['index_aux'] < int(i*(1/k)*X.shape[0]))]
            X_train = X[(X['index_aux'] > int(i*(1/k)*X.shape[0]))]

            Y_test = Y[:int(i*(1/k)*Y.shape[0])]
            Y_train = Y[int(i*(1/k)*Y.shape[0]):]

            ## -- Executando o Purge em cima dos dados

            X_train = X_train[ X_train.index > conta_segundos(str(X_train.index[0]), purge) ] # > first_date + purge

            X_test = X_test [ X_test.index < conta_segundos(str(X_test.index[-1], -purge) ] # < last_date - purge

            Y_train = Y_train[ Y_train.index > conta_segundos(str(Y_train.index[0]), purge) ] # > first_date + purge

            Y_test = Y_test[ Y_test.index > conta_segundos(str(Y_test.index[0]), purge) ] # < last_date - purge

            # Eliminando os index aux

            X_train.drop(["index_aux"], axis=1, inplace=True)
            X_test.drop(["index_aux"], axis=1, inplace=True)
            Y_train.drop(["index_aux"], axis=1, inplace=True)
            Y_test.drop(["index_aux"], axis=1, inplace=True)

            print("[INFO] X_test.shape: ", X_test.shape)
            print("[INFO] X_train.shape: ", X_train.shape)

            ## -- Escalando os dados

            if scaler != None:

                X_train = scaler.fit_transform(X_train)
                X_test = scaler.fit_transform(X_test)

            ## -- Aplicando um PCA, eventualmente
            
            #
            #
            #

            ## -- Treinando o Modelo

            model.fit(X_train, Y_train)

            Y_pred = model.predict(X_test)

            ## -- Calculando r2 score

            metrics.append(score_metric(Y_pred, Y_test))

            ## -- Calculando backtest

            #
            #
            #
        
        if (i != 1) and (i != K):

            X_train = X[ (X['index_aux'] < int(i*(1/k)*X.shape[0])) & (X['index_aux'] > int((i+1)*(1/k)*X.shape[0])) ]

            X_test = X[ (X['index_aux'] > int(i*(1/k)*X.shape[0])) & (X['index_aux'] < int((i+1)*(1/k)*X.shape[0])) ]

            Y_train = Y[ (Y['index_aux'] < int(i*(1/k)*Y.shape[0])) & (Y['index_aux'] > int((i+1)*(1/k)*Y.shape[0])) ]

            Y_test = Y[ (Y['index_aux'] > int(i*(1/k)*Y.shape[0])) & (Y['index_aux'] < int((i+1)*(1/k)*Y.shape[0])) ]

            ## -- Executando o Purge em cima dos dados

            X_train = X_train[ (X_train.index < conta_segundos(str(X_test.index[0]), -purge)) & (X_train.index > conta_segundos(str(X_test.index[-1]), purge)) ] 
            
            X_test = X_test[ (X_test.index > conta_segundos(str(X_test.index[0]), purge)) & (X_test.index < conta_segundos(str(X_test.index[-1]), -purge)) ]

            Y_train = Y_train[ (Y_train.index < conta_segundos(str(X_test.index[0]), -purge)) & (Y_train.index > conta_segundos(str(X_test.index[-1]), purge)) ]

            Y_test = Y_test[ (Y_test.index > conta_segundos(str(X_test.index[0]), purge)) & (Y_test.index < conta_segundos(str(X_test.index[-1]), -purge)) ]

            ## -- Eliminando os index aux

            X_train.drop(["index_aux"], axis=1, inplace=True)
            X_test.drop(["index_aux"], axis=1, inplace=True)
            Y_train.drop(["index_aux"], axis=1, inplace=True)
            Y_test.drop(["index_aux"], axis=1, inplace=True)

            print("[INFO] X_test.shape: ", X_test.shape)
            print("[INFO] X_train.shape: ", X_train.shape)

            ## -- Escalando os dados

            if scaler != None:

                X_train = scaler.fit_transform(X_train)
                X_test = scaler.fit_transform(X_test)

            ## -- Aplicando um PCA, eventualmente
            
            #
            #
            #

            ## -- Treinando o Modelo

            model.fit(X_train, Y_train)

            Y_pred = model.predict(X_test)

            ## -- Calculando r2 score

            metrics.append(score_metric(Y_pred, Y_test))

            ## -- Calculando backtest

            #
            #
            #

        if i == K:

            X_train = X[ X['index_aux'] < int((i-1)*(1/k)*X.shape[0]) ]

            X_test = X[ X['index_aux'] > int((i-1)*(1/k)*X.shape[0]) ]

            Y_train = Y[ Y['index_aux'] < int((i-1)*(1/k)*Y.shape[0]) ]

            Y_test = Y[ Y['index_aux'] > int((i-1)*(1/k)*Y.shape[0]) ]

            ## -- Executando o Purge em cima dos dados

            X_train = X_train[ X_train.index < conta_segundos(str(X_test.index[0]), -purge) ]

            X_test = X_test[ X_test.index > conta_segundos(str(X_test.index[0]), purge) ]


            ## -- Eliminando os index aux

            X_train.drop(["index_aux"], axis=1, inplace=True)
            X_test.drop(["index_aux"], axis=1, inplace=True)
            Y_train.drop(["index_aux"], axis=1, inplace=True)
            Y_test.drop(["index_aux"], axis=1, inplace=True)

            print("[INFO] X_test.shape: ", X_test.shape)
            print("[INFO] X_train.shape: ", X_train.shape)

            ## -- Escalando os dados

            if scaler != None:

                X_train = scaler.fit_transform(X_train)
                X_test = scaler.fit_transform(X_test)

            ## -- Aplicando um PCA, eventualmente
            
            #
            #
            #

            ## -- Treinando o Modelo

            model.fit(X_train, Y_train)

            Y_pred = model.predict(X_test)

            ## -- Calculando r2 score

            metrics.append(score_metric(Y_pred, Y_test))

            ## -- Calculando backtest

            #
            #
            #

    return metrics




            




