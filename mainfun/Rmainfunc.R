## logistic regression (train data)
data = read.csv("E:\\etl\\mainfun\\traindata.csv",header = FALSE)
library(caTools)
spl = sample.split(data$V5, SplitRatio = 1)
ClaimsTrain = subset(data, spl==TRUE)
table(ClaimsTrain$V5)
ClaimsTest = subset(data, spl==FALSE)
#V4不顯著不使用，glm-->logistic regression
y = glm(V5~V1+V2+V3,data = data) 
#V5~V1+V2+V3 : V5 = aV1+bV2+cV3 ；v5:應變數、V1~V3:自變數
PredictTest = predict(y, newdata = ClaimsTest, type = "response")
table(ClaimsTest$V5, PredictTest>0.7)

#library(ROCR)
## 繪製 ROC curve (x-axis: FPR, y-axis: TPR)
## https://zh.wikipedia.org/wiki/ROC%E6%9B%B2%E7%BA%BF
#pred = prediction(PredictTest,ClaimsTest$V5)
#perf = performance(pred,"tpr","fpr")
#plot(perf)
#as.numeric(performance(pred,"auc")@y.values)


## logistic regression_real 
ClaimsTest = read.csv("E:\\etl\\mainfun\\mainfun.csv",header = FALSE)
PredictTest = predict(y, newdata = ClaimsTest, type = "response")
library(car)
if(any(PredictTest >0.7)){
  ifelse (PV <- PredictTest>0.7,1,0)
  }else{PV <- recode(PredictTest,"max(PredictTest)=1;else =0")}

value = list('staff'=ClaimsTest$V5,'mainMelody'=PV)
RR <- as.data.frame(value)

write.csv(RR, file = "E:\\etl\\mainfun\\MyData.csv",row.names=FALSE)

