## Define exact goal of model

1. will it be supervised or unsupervised

2. should it be treated as time series (importance of time)

3. what parameters should be the features and what parameter should be the label

4. should I drop columns such as BW, SF, CR because of calculated DR contains indirectly all of those

## What is already done

- data loading

- data preparation

- data cleaning

- data split

- papers read: A study of LoRa: Long Range & Low Power Networks for the IoT
	       Analysis of the Capacity and Scalability of the LoRa WAN Technology

- papers to read: Analysis of Latency and MAC Performance for Class A LoRaWAN
                  Decoding LoRa PHY by Matt Knight from POC||GTFO magazine

- created simple script to model LoRa signal and waveform, together w/ its spectrogram

## Conclusion

1. supervised, define target through ACK messages

2. it should be treated as times series - probability of success will be larger in bigger time periods

3. check (2) for target, labels will be time period, rssi, snr, data rate, code rate, bw and spreading factor

4. no, different combinations of BW, SF & CR can result in the same DR value

## Next steps

- draw topology model of the Svebolle deployment - asap!

- go through Bayesian Inference notebook from PyCon 2017 conference

- Fitting Regression Models (PyCon2017 & Aurelian Geron)
