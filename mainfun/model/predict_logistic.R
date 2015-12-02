## logistic regression
##install.packages("caTools") 
##library(caTools) 
data = read.csv("data2.csv",header = FALSE)
spl = sample.split(data$V5, SplitRatio = 0.8)
ClaimsTrain = subset(data, spl==TRUE)
ClaimsTest = subset(data, spl==FALSE)
#V4不顯著不使用，glm-->logistic regression
y = glm(V5~V1+V2+V3,data = data, family = "binomial")
#response，predict回傳機率值(預設為勝算比log-odds)
PredictTest = predict(y, newdata = ClaimsTest, type = "response")
table(ClaimsTest$V5, PredictTest>0.6)

#library(ROCR)
## 繪製 ROC curve (x-axis: FPR, y-axis: TPR)
## https://zh.wikipedia.org/wiki/ROC%E6%9B%B2%E7%BA%BF
pred = prediction(PredictTest,ClaimsTest$V5)
perf = performance(pred,"tpr","fpr")
plot(perf)
#ROC curve下所佔面積
as.numeric(performance(pred,"auc")@y.values)
  
## linear regression
data = read.csv("data2.csv",header = FALSE)
spl = sample.split(data$V5, SplitRatio = 0.7)
ClaimsTrain = subset(data, spl==TRUE)
ClaimsTest = subset(data, spl==FALSE)
#V4不顯著不使用，lm-->linear regression
y2 = lm(V5~V1+V2+V3,data = data)
PredictTest2 = predict(y2, newdata = ClaimsTest, type = "response")
table(ClaimsTest$V5, PredictTest2>0.5)

# summary 可計算 5 大統計值: Min, 1st Qu. , Median, Mean, 3rd Qu., Max.
summary(PredictTest2)