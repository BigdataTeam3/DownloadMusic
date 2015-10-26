  ## logistic regression
data = read.csv("data2.csv",header = FALSE)
spl = sample.split(data$V5, SplitRatio = 0.8)
ClaimsTrain = subset(data, spl==TRUE)
ClaimsTest = subset(data, spl==FALSE)
y = glm(V5~V1+V2+V3,data = data, family = "binomial")
PredictTest = predict(y, newdata = ClaimsTest, type = "response")
table(ClaimsTest$V5, PredictTest>0.6)

pred = prediction(PredictTest,ClaimsTest$V5)
perf = performance(pred,"tpr","fpr")
plot(perf)
as.numeric(performance(pred,"auc")@y.values)
  ## linear regression
data = read.csv("data2.csv",header = FALSE)
spl = sample.split(data$V5, SplitRatio = 0.7)
ClaimsTrain = subset(data, spl==TRUE)
ClaimsTest = subset(data, spl==FALSE)
y2 = lm(V5~V1+V2+V3,data = data)
PredictTest2 = predict(y2, newdata = ClaimsTest, type = "response")
table(ClaimsTest$V5, PredictTest>0.5)

summary(PredictTest2)