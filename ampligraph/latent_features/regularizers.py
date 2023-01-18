from functools import partial
import tensorflow as tf


def LP_regularizer(trainable_param, regularizer_parameters={}):
    '''Norm :math:`L^{p}` regularizer.

    It is passed to the model as the ``entity_relation_regularizer`` argument of the
    :meth:`~ampligraph.latent_features.models.ScoringBasedEmbeddingModel.compile` method.

    Parameters
    ----------
    trainable_param: tf.Variable
        Trainable parameters of the model that need to be regularized.
    regularizer_parameters: dict
        Parameters of the regularizer:

        - **p**: (int) - p for the LP regularizer. For example, when :math:`p=3` (default), it uses the L3 regularizer.
        - **lambda** : (float) - Regularizer weight (default: 0.001).
    Returns
    -------
    regularizer: tf.keras.regularizer
        Regularizer instance from the `tf.keras.regularizer` class.

    '''
    return regularizer_parameters.get('lambda', 0.001) * tf.reduce_sum(
        tf.pow(tf.abs(trainable_param), regularizer_parameters.get('p', 3)))


def get(identifier, hyperparams={}):
    ''' Get the regularizer specified by the identifier.

    Parameters:
    -----------
    identifier: str or tf.keras.regularizer or a callable
        Name of the regularizer to use (with default parameters) or instance of `tf.keras.regularizer` or a
        callable function.

    Returns:
    --------
    regularizer: tf.keras.regularizer
        Regularizer instance of the `tf.keras.regularizer` class.

    '''
    if isinstance(identifier, str) and identifier == 'l3':
        hyperparams['p'] = 3
        identifier = partial(LP_regularizer, regularizer_parameters=hyperparams)
        identifier = tf.keras.regularizers.get(identifier)
        identifier.__name__ = 'LP'
    elif isinstance(identifier, str) and identifier == 'LP':
        identifier = partial(LP_regularizer, regularizer_parameters=hyperparams)
        identifier = tf.keras.regularizers.get(identifier)
        identifier.__name__ = 'LP'
    return identifier
