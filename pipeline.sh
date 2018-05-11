if [[ $# -ne 1 ]]
then
echo "Enter Correct number of arguments"
exit 1
fi

IFN=$1

cd SequenceLabelingWithCRF-master/
rm -r stories
mkdir stories
python3 predict_dial_tags.py $IFN stories/
echo "Done making articles"
cd ..
rm -r stories_tokenized
mkdir stories_tokenized
python3 make_datafiles.py SequenceLabelingWithCRF-master/stories/ val.bin
echo "binary file created in finished_files with name val.bin"
cp -r /home/saket/Desktop/nlp/Project/pretrained_model/decode_val_600maxenc_4beam_80mindec_150maxdec_ckpt-238410 logs/
rm -r /home/saket/Desktop/nlp/Project/pretrained_model/decode_val_600maxenc_4beam_80mindec_150maxdec_ckpt-238410
cd pointer-generator-master
python3 run_summarization.py --mode=decode --data_path=/home/saket/Desktop/nlp/Project/finished_files/val.bin --vocab_path=/home/saket/Desktop/nlp/Project/finished_files/vocab --log_root=/home/saket/Desktop/nlp/Project/ --exp_name=pretrained_model --coverage=1 --single_pass=1 --min_dec_steps=80 --max_dec_steps=150 --max_enc_steps=600
cd ..
echo "Done generating summary"
cd ROUGE-2.0/distribute/
cp /home/saket/Desktop/nlp/Project/pretrained_model/decode_val_600maxenc_4beam_80mindec_150maxdec_ckpt-238410/decoded/* test-summarization/system/ 
cp -r /home/saket/Desktop/nlp/Project/pretrained_model/decode_val_600maxenc_4beam_80mindec_150maxdec_ckpt-238410/reference/ test-summarization/
java -jar rouge2.0_0.2.jar 