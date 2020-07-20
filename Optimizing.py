import pandas as pd
import copy
import numpy as np
import math


#parent Class
class Pipe:
    
    # Initializer / Instance Attributes
    def __init__(self, name, weight,quantity,clearence):
        self.name = str(name)
        #self.shape = shape
        self.weight=weight
        self.quantity=quantity
    
    

#Class for circular pipes
class Circle(Pipe):
    def __init__(self,name,shape,daimeter,thickness,lenght,quantity,weight,clearence):
        Pipe.__init__(self,name,weight,quantity,clearence)
        self.shape=shape
        self.daimeter=daimeter
        self.thickness=thickness
        self.lenght=lenght
        self.area= (np.pi*(daimeter**2))/4
        self.inner=daimeter-(2*clearence)
        self.innerArea= (np.pi*(self.inner**2))/4
        self.outterDaimeter= daimeter+(2*clearence)
        self.sequence=[name]
        self.numberOfPipes=1
        self.innerMostShape="Circle"
        self.outter=self.outterDaimeter
        self.height=self.outterDaimeter
        
    def checkToInsert(self,sorted_list):
        l=len(sorted_list)
        returnObj=[]
        for i in range(l):
            if(sorted_list[i].shape=="Circle"): #For circle
                if(self.inner>sorted_list[i].outterDaimeter):
                    returnObj.append(sorted_list[i])
            else: #Square and Rectangle
                if(self.inner>sorted_list[i].outterDiagonal):
                    returnObj.append(sorted_list[i])
        #print("Number of fits = ",len(returnObj))
        return returnObj
    
    
    
#Class for Rectangle pipes pipes
class Rectangle(Pipe):
    
    def __init__(self,name,shape,width,length,thickness,weight,quantity,clearence):
        Pipe.__init__(self,name,weight,quantity,clearence)
        self.shape=shape
        self.width=width
        self.length=length
        self.outterLength=length+(2*clearence)
        self.outterWidth=width+(2*clearence)
        self.innerLength=length-(2*clearence)
        self.inner=width-(2*clearence)
        self.diagonal= np.sqrt(length**2+width**2)
        self.outterDiagonal=self.diagonal+(2*clearence)
        self.innerDiagonal=self.diagonal-(2*clearence)
        self.area=self.length*self.width
        self.outterArea=(self.length+(clearence*2))*(self.width+(clearence*2))
        self.innerArea=(self.length-(clearence*2))*(self.width-(clearence*2))
        self.sequence=[name]
        self.numberOfPipes=1
        self.innerMostShape='Rectangle'
        self.outter=self.outterLength
        self.height=self.outterWidth
        
    def checkToInsert(self,sorted_list):
        l=len(sorted_list)
        returnObj=[]
        #its a square
        for i in range(l):
            if(sorted_list[i].shape=="Circle"):
                if(sorted_list[i].outterDaimeter<self.inner):
                    returnObj.append(sorted_list[i])
            elif(sorted_list[i].width==sorted_list[i].length):
                #only sqr, not rectangle
                if(sorted_list[i].outterLength<self.inner):
                    returnObj.append(sorted_list[i])
            else:
                if(self.innerMostShape=="Rectangle"):
                    if(sorted_list[i].width<self.inner and sorted_list[i].length<self.innerLength):
                        returnObj.append(sorted_list[i])
                if(self.innerMostShape=="Circle"):
                    if(sorted_list[i].inner<self.inner):
                        returnObj.append(sorted_list[i])
        return returnObj
    
  
    
def removePipeName(objs,nameToDel):
    for obj in objs:
        if(obj.name==nameToDel):
            objs.remove(obj)
            break


#Creating loading list
def loading_List(listOfObj):
    load=[]
    while(len(listOfObj)!=0):
        pipe=listOfObj[0]
        fits=pipe.checkToInsert(listOfObj[1:])
        newPipe=pipe
        if(len(fits)==0):
            load.append(newPipe)
            removePipeName(listOfObj,newPipe.name)

        else:
            fitPipe=fits[0]

            newPipe=copy.deepcopy(pipe)
            newPipe.name=str(newPipe.name)+"->"+str(fitPipe.name)
            newPipe.sequence.append(fitPipe.name)
            newPipe.numberOfPipes=newPipe.numberOfPipes+1
            newPipe.weight=newPipe.weight+fitPipe.weight
            newPipe.inner=fitPipe.inner
            newPipe.innerMostShape=fitPipe.innerMostShape
            if(pipe.quantity>fitPipe.quantity):
                pipe.quantity=pipe.quantity-fitPipe.quantity
                newPipe.quantity=fitPipe.quantity
                removePipeName(listOfObj,fitPipe.name)
            elif(pipe.quantity<fitPipe.quantity):
                fitPipe.quantity=fitPipe.quantity-pipe.quantity
                newPipe.quantity=pipe.quantity
                removePipeName(listOfObj,pipe.name)
            elif(pipe.quantity==fitPipe.quantity):
                newPipe.quantity=pipe.quantity
                listOfObj.remove(item.name==pipe.name)
                listOfObj.remove(item.name==fitPipe.name)
            listOfObj.insert(0,newPipe)

    return load



#Final Truck 1



def Final_loading(load,l_height,l_weight,l_width):

    
    l_height=int(l_height)
    l_weight=int(l_weight)
    l_width=int(l_width)
    
    output=[]
    
    truck=[]
    t_height=0
    t_weight=0
    
    rows=[]
    total_row_count=1
    row=[]
    i=0
    j=0
    t=1
    

    
    
    for j in range(len(load)+5):
        try:
            pipe=load[j]
        except IndexError:
            print("DONE")
            return output;

        i=i+1
        uniqueType=[]
        s= "\n"+str(i)+") Name-  "+ str(pipe.name)+ "\n"
        uniqueType.append(s)
        
        s="Pipe Quantity- "+str(pipe.quantity)+", Height ="+str(pipe.height)+', Widht='+str( pipe.outter)+"\n"
        uniqueType.append(s)

        pipeCountPerRow=int(l_width/pipe.outter)
        rowCount=math.ceil(pipe.quantity/pipeCountPerRow)
        s= "Count of pipes per row= "+str(pipeCountPerRow)
        uniqueType.append(s)
        s="Number of rows- "+str(rowCount)+" with height= "+str(pipe.height*rowCount)
        uniqueType.append(s)

        if((t_height+(pipe.height*rowCount))>l_height):
            rowCount=math.ceil((l_height-t_height)/pipe.height)
            q=rowCount*pipeCountPerRow
            pipe.quantity=pipe.quantity-q
            t_weight=t_weight+(pipe.weight*q)
            
            
            uniqueType=[]

            s="\n"+str(q)+" Pipes Loaded, rest to be put in next truck" 
            uniqueType.append(s)

            s="Height will exceded"
            uniqueType.append(s)

            s="TRUCK "+str(t)+" full"
            uniqueType.append(s)

            t=t+1
            s="Start filling in TRUCK "+str(t)
            uniqueType.append(s)
            

            s=" ################################################ "
            uniqueType.append(s)
            output.append(uniqueType)
            
            t_weight=0
            t_height=0
            load.insert(j,pipe)
            j=j-2
            continue
        if((t_weight+(pipe.quantity*pipe.weight))>l_weight):
            q=math.ceil((l_weight-t_weight)/pipe.weight)
            pipe.quantity=pipe.quantity-q
            t_weight=t_weight+(pipe.weight*q)
            t=t+1
            uniqueType=[]
            s="Pipes Loaded, rest to be put in next truck"
            uniqueType.append(s)
            
            s="Weight Limit Exceded"
            uniqueType.append(s)
            
            s="TRUCK "+str(t)+"  full "
            uniqueType.append(s)
            
            output.append(uniqueType)

            t_weight=0
            t_height=0
            load.insert(j,pipe)
            j=j-2
            continue
        t_weight=(pipe.weight*pipe.quantity)+t_weight
        t_height=t_height+pipe.height*rowCount



        
        s="Current Weight = "+str(t_weight)
        uniqueType.append(s)
        s=" Current Height = "+str(t_height)
        uniqueType.append(s)
        output.append(uniqueType)
        
    return output




def Optimize_loading(path="Pipe2.csv",clearence=2, height_limit=2133,weight_limit=25000,width_limit=2286):
    data=pd.read_csv(path)


    #clearence=2


    #Create 
    types=[]
    for i in range(len(data)):
        sp=str(data.iloc[i]['Specification(mm)'])
        specs=sp.split("*")
        for j in range(len(specs)):
            specs[j]=float(specs[j])
        if(data.iloc[i]["Shape"]=="Circle"):
            types.append(Circle(data.iloc[i]["No."],data.iloc[i]["Shape"],specs[0],specs[1],specs[2],int(data.iloc[i]["Quantity \n(PCS)"]),float(data.iloc[i]['per piece wt']),clearence))
        else:
            types.append(Rectangle(data.iloc[i]["No."],data.iloc[i]["Shape"],specs[1],specs[0],specs[2],int(data.iloc[i]['per piece wt']),float(data.iloc[i]["Quantity \n(PCS)"]),clearence))



    #Sort according to area
    new_types=sorted(types,key=lambda x:x.area,reverse=True)
    listOfObj=new_types

    loaded_list=loading_List(listOfObj)
    
    
    s2=Final_loading(load=loaded_list,l_height=height_limit,l_weight=weight_limit,l_width=width_limit)
    
    
    return s2








