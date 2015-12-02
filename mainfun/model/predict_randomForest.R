  ## linear regression
data = read.csv("C:\\Users\\BigData\\python\\data2.csv",header = FALSE)
spl = sample.split(data$V5, SplitRatio = 0.7)
ClaimsTrain = subset(data, spl==TRUE)
ClaimsTest = subset(data, spl==FALSE)
#V4不顯著不使用，lm-->linear regression
y2 = lm(V5~V1+V2+V3,data = data)
PredictTest2 = predict(y2, newdata = ClaimsTest, type = "response")
table(ClaimsTest$V5, PredictTest2>0.7)

summary(PredictTest2)
 ## random forest
data = read.csv("C:\\Users\\BigData\\python\\data3.csv",header = FALSE)
spl = sample.split(data$V5, SplitRatio = 0.7)
ClaimsTrain = subset(data, spl==TRUE)
table(ClaimsTrain$V5)
ClaimsTest = subset(data, spl==FALSE)
#V4不顯著不使用，randomForest-->random forest
y = randomForest(V5~V1+V2+V3,data = data)
PredictTest = predict(y, newdata = ClaimsTest, type = "response")
table(ClaimsTest$V5, PredictTest>0.7)
#library(ROCR)
## 繪製 ROC curve (x-axis: FPR, y-axis: TPR)
## https://zh.wikipedia.org/wiki/ROC%E6%9B%B2%E7%BA%BF
pred = prediction(PredictTest,ClaimsTest$V5)
perf = performance(pred,"tpr","fpr")
plot(perf)
as.numeric(performance(pred,"auc")@y.values)