args <- commandArgs(trailingOnly = TRUE)
action <- args[1]
#past(action)
#print (action)

#getwd()
library("ChemmineR")
apold1 <- cmp.parse("drugnew.sdf")
aplist1 <- apold1[[1]]; names(aplist1) <- apold1[[2]]
apset1 <- as(aplist1, "APset")
#save(apset1, file = "apset1.rda", compress = TRUE)

apold2 <- cmp.parse(action)
aplist2 <- apold2[[1]]; names(aplist2) <- apold2[[2]]
apset2 <- as(aplist2, "APset")
#save(apset2, file = "apset2.rda", compress = TRUE)
#load("apset1.rda")
#load("apset2.rda")
x<-cmp.search(apset1, apset2, type=3, cutoff = 0.3)
write.csv(x, file = "output.csv")
