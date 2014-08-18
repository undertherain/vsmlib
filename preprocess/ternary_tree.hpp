char  buffer[255];
//unsigned long long cnt_words;
//std::ofstream file;

Index id=1;

template <typename T>
class TernaryTreeNode
{
public:
    char c;
    TernaryTreeNode * left;
    TernaryTreeNode * down;
    TernaryTreeNode * right;
    T data;
};

template <typename T>
void set_id(TernaryTreeNode<T> * node, const char * str)
{
/*  if (head==NULL)
    { 
        head= new TernaryTreeNode<T>();
        head->c=str[0];
    }*/ 
    //TernaryTreeNode<T> * node = head;
    unsigned int depth=0;
    while (depth<strlen(str)-1)
    {
        char c=str[depth];
        if (c==node->c)
        {
            if (node->down==NULL) 
            {
                node->down= new TernaryTreeNode<T>();
                node->down->c=str[depth+1];     
            }
            node=node->down;
            depth++;
            continue;
        } 
        if (c<node->c)
        {
            if (node->left==NULL)   
            {   
                node->left= new TernaryTreeNode<T>();
                node->left->c=c;
            }
            node=node->left;
            continue;
        } 
        if (c>node->c)
        {
            if (node->right==NULL) 
            {
                node->right= new TernaryTreeNode<T>();
                node->right->c=c;
            }
            node=node->right;
            //continue;
        }
    }
    if (!node->data) node->data=id++;
}


template <typename T>
void increment(TernaryTreeNode<T> * node, const char * str)
{
/*  if (head==NULL)
    { 
        head= new TernaryTreeNode<T>();
        head->c=str[0];
    }*/ 
    //TernaryTreeNode<T> * node = head;
    unsigned int depth=0;
    while (depth<strlen(str)-1)
    {
        char c=str[depth];
        if (c==node->c)
        {
            if (node->down==NULL) 
            {
                node->down= new TernaryTreeNode<T>();
                node->down->c=str[depth+1];     
            }
            node=node->down;
            depth++;
            continue;
        } 
        if (c<node->c)
        {
            if (node->left==NULL)   
            {   
                node->left= new TernaryTreeNode<T>();
                node->left->c=c;
            }
            node=node->left;
            continue;
        } 
        if (c>node->c)
        {
            if (node->right==NULL) 
            {
                node->right= new TernaryTreeNode<T>();
                node->right->c=c;
            }
            node=node->right;
            //continue;
        }
    }
    node->data+=1;
}

template <typename T>
T get_value(const TernaryTreeNode<T> * node, const char * str)
{
    unsigned int depth=0;
    while (depth<strlen(str)-1)
    {
        char c=str[depth];
        if (c==node->c)
        {
            if (node->down==NULL) return 0;
            node=node->down;
            depth++;
            continue;
        } 
        if (c<node->c)
        {
            if (node->left==NULL)  return 0;
            node=node->left;
            continue;
        } 
        if (c>node->c)
        {
            if (node->right==NULL) return 0;
            node=node->right;
        }
    }
    return node->data;
}


template <typename T>
void traverse(const TernaryTreeNode<T> * node,unsigned int depth)
{
    buffer[depth]=node->c;  
    if (node->data)
    file<<std::string(buffer,buffer+depth+1)<<"\t"<<node->data<<"\n";
    if (node->left!=NULL) traverse<T>(node->left,depth);
    buffer[depth]=node->c;  
    if (node->down!=NULL) traverse<T>(node->down,depth+1);
    buffer[depth]=node->c;  
    if (node->right!=NULL) traverse<T>(node->right,depth);
    buffer[depth]=node->c;  
}

