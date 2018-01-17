#------------------------------------------------------------------------------
# VSMLib configuration
#------------------------------------------------------------------------------

## The root path of dataset to be evaluated
c.Evaluate.path_root_dataset = '/work/data/NLP/datasets/'

## The root path of yaml configuration file
c.Evaluate.path_root_config = './vsmlib/benchmarks/'

## The evaluation details of each task
c.Evaluate.test_word_similarity = True
c.Evaluate.word_similarity.config_folder_name = 'similarity'
c.Evaluate.word_similarity.dataset_folder_name = 'similarity'

c.Evaluate.test_word_analogy_google = False
c.Evaluate.word_analogy_google.config_folder_name = 'analogy'
c.Evaluate.word_analogy_google.dataset_folder_name = 'analogies/Google_dir'

c.Evaluate.test_word_analogy_bats = False
c.Evaluate.word_analogy_bats.config_folder_name = 'analogy'
c.Evaluate.word_analogy_bats.dataset_folder_name = 'analogies/BATS_3.0'

c.Evaluate.test_sequence_labeling = False
c.Evaluate.sequence_labeling.config_folder_name = 'sequence_labeling'
c.Evaluate.sequence_labeling.dataset_folder_name = 'sequence_labeling'
c.Evaluate.sequence_labeling.subtasks = ['pos', 'chunk', 'ner']

## The default keys which used to generate the evaluation results folder from evaluation json result
c.Evaluate.folder_name_keys = ['task', 'dataset', 'method', 'measurement']

## The default keys which used to generate the embedding results folder from embedding meta data
c.Embedding.folder_name_keys = ['model', 'negative_size', 'epoch', 'window', 'batchsize']