#this function load blogdata.txt; return three vars: colnames, rownames, data. test: if True, load 2 column data to test. False: load all data. Array: return colnames, rownames, and an array data. DataFrame: return a dataFrame, the most recommended one.

def loadData(filename,test = True,Array = False, DataFrame = False):
        filePath = 'data/clusters/'
        data = []
        colnames = []
        rownames = []
        lines = [line for line in open(filePath+filename)]
        #colnames is keywords, rownames is users' name
        colnames = lines[0].strip().split('\t')[1:]
        if test:
                lines = lines[1:4]
        else:
                lines = lines[1:]
        for line in lines:
                temp = line.strip().split('\t')
                rownames.append(temp[0])
                data.append([float(x) for x in temp[1:]])
                # data could also be saved in dict: data.setdefault(temp[0],[float(x) for x in temp[1:]])
        if Array:
                import numpy as np
                return colnames, rownames, np.array(data,dtype = np.float32)
        elif DataFrame:
                import numpy as np
                data = np.array(data,dtype = np.float32)
                import pandas as pd
                df = pd.DataFrame(data,columns = colnames,index = rownames)
                return df
        else:
                return colnames, rownames, data
def pearson(vec1,vec2):
        from math import sqrt
        length = min([len(vec1),len(vec2)])
        sum1 = sum(vec1)
        sum2 = sum(vec2)
        sum1Sq = sum([pow(i,2) for i in vec1])
        sum2Sq = sum([pow(i,2) for i in vec2])
        pSum = sum([vec1[i]*vec2[i] for i in range(length)])
        num = pSum - (sum1*sum2/length)
        den = sqrt((sum1Sq - pow(sum1,2)/length)*(sum2Sq - pow(sum2,2)/length))
        if den == 0 :
                return 0
        else:
                return 1.0- num/den
#create a binary tree, and bicluster is the node of this tree. Data: vec, left, right, distance: distance between left node and right node.
class bicluster:
    def __init__(self,vec,left= None, right = None, distance = pearson, id = None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
#create an binary tree, 
def hcluster (rows, distance = pearson):
    allCluster = [bicluster(rows[i], id = i) for i in range(len(rows))]
    distances = {}
    newClusterID  = -1
    while(len(allCluster) > 1):
        lowest_position = (0,1)
        min_distance  = pearson(allCluster[0].vec,allCluster[1].vec)
        for i in range(len(allCluster)):
            for j in range(i+1,len(allCluster)):
                #use distances(a dictionary) to buffer distances between clusters.
                if (allCluster[i].id,allCluster[j].id) not in distances:
                    distances[(allCluster[i].id,allCluster[j].id)] =  pearson(allCluster[i].vec,allCluster[j].vec)
                temp = distances[(allCluster[i].id,allCluster[j].id)]
                if temp < min_distance:
                    min_distance = temp
                    lowest_position = (i,j)
        #newNode is the parent node of two lowest cluster. rows cannot be parent node, only new node could. And new nodes' ID is less than 0: -1, -2, -3 
        # attention: lowest_position = ()
        newVec = [(allCluster[lowest_position[0]].vec[i]+allCluster[lowest_position[1]].vec[i])/2.0 for i in range(len(allCluster[0].vec))]
        newNode = bicluster(newVec,left = allCluster[lowest_position[0]], right = allCluster[lowest_position[1]], distance = min_distance, id = newClusterID)           
        newClusterID -= 1               
        allCluster.append(newNode)
        del allCluster[lowest_position[0]]
        del allCluster[lowest_position[1]-1]
    return allCluster[0]
def visit(cluster):
    if cluster.left != None:
        print('left child: '+ str(cluster.left.id),end = '\n')
        visit(cluster.left)
    if cluster.right != None:
        print('right child: '+ str(cluster.right.id),end = '\n')
        visit(cluster.right)
    return 0
def getHeight(cluster):
    if cluster.left == None and cluster.right == None:
        return 1
    else:
        return getHeight(cluster.left) + getHeight(cluster.right)
def getDepth(cluster):
    if cluster.left ==None and cluster.right == None:
        return 0.0
    else:
        return max(getDepth(cluster.left), getDepth(cluster.right)) + cluster.distance
def drawNode(draw,cluster,x,y,scaling,labels):
        if cluster.id<0:
                height1 = getHeight(cluster.left)*20
                height2 = getHeight(cluster.right)*20
                top = y -(height1+height2)/2
                bottom = y + (height1+height2)/2
                # line length
                length_line = cluster.distance * scaling
                draw.line((x,top+height1/2,x,bottom-height2/2),fill = (255,0,0))
                draw.line((x,top+height1/2,x+length_line,top+height1/2),fill = (255,0,0))
                draw.line((x,bottom - height2/2 , x+length_line , bottom- height2/2),fill = (255,0,0))
                drawNode(draw,cluster.left,x+length_line,top+height1/2,scaling,labels)
                drawNode(draw,cluster.right,x+length_line,bottom - height2/2,scaling,labels)
        else:  
                # if this is a leaf node.
                draw.text((x+5,y-7),labels[cluster.id],(0,0,0))
def drawDendrogram(cluster,labels,jpeg = 'clusters.jpg'):
    height = getHeight(cluster)*20
    width = 1200
    scaling = (width-150)/getDepth(cluster)
    from PIL import Image, ImageDraw
    img = Image.new('RGB',(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.line((0,height/2,10,height/2),fill = (255,0,0))
    drawNode(draw,cluster,10,height/2,scaling,labels)
    img.save(jpeg,'JPEG')
def rotateMatrix(data):
    newData = []
    for i in range(len(data[0])):
        newRow = [data[j][i] for j in range(len(data))]
        newData.append(newRow)
    return newData
def kCluster(data, distance = pearson, k = 4):
    import random
    # save the index of centers in data. 
    centers = []
    clusters = []
    for i in range(k):
        centers.append(data[random.randint(0,len(data)-1)])
        assert len(centers) == k, 'the num of center isn\'t equal to k'
    
        for i in range(len(data)):
                temp_distance = distance(data[i],centers[0])
                for j in range(len(centers)):
                        if distance(data[i], centers[j]) < temp_distance:
                                temp_distance = distance(data[i],centers[j])
                                #attention: time to classification, save all nodes into class.
                                clusters[j].append(i)
if __name__ == '__main__':
    keywords, users, data = loadData('blogdata.txt',test = False)
    clust = hcluster(data)
    visit(clust)
    drawDendrogram(clust,users)
