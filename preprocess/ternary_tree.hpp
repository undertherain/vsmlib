char  buffer[255];
//unsigned long long cnt_words;
//std::ofstream file;

Index id_global=0;

template <typename T>
class TernaryTreeNode
{
public:
    char c;
    TernaryTreeNode * left;
    TernaryTreeNode * down;
    TernaryTreeNode * right;
    T data;
    Index id;
};

void check_tree()
{
/*
    set_id_and_increment(tree,"cat");
    set_id_and_increment(tree,"cax");
    set_id_and_increment(tree,"banana");
    //set_id_and_increment(tree,"applx");
    std::cerr <<"frequencies:\n";
    dump_frequency(std::cerr, tree,0);
    std::cerr <<"ids:\n";
    dump_ids(std::cerr, tree,0);
    get_id(tree,"cat");
    get_id(tree,"cax");
    get_id(tree,"banana");
  */  
//    return 0;
}
    
Index set_id_and_increment(TernaryTreeNode<Index> * node, const char * str)
{
/*  if (head==NULL)
    { 
        head= new TernaryTreeNode<T>();
        head->c=str[0];
    }*/ 
    //TernaryTreeNode<T> * node = head;
    unsigned int depth=0;
    bool is_done=false;
//    while (depth<strlen(str)-1)
    while (!is_done)
    {
        char c=str[depth];
        //std::cerr<<"depth = "<<depth<<"\tnode.c = "<<node->c<<"\tc = "<<c<<"\n";
        if (c==node->c)
        {
            if (node->down==NULL) 
            {
                node->down= new TernaryTreeNode<Index>();
                node->down->c=str[depth+1];     
                //std::cerr<<"creating down\n";
            }
            node=node->down;
            //std::cerr<<"moving down\n";
            depth++;
            c=str[depth];
           // continue;
        } else
        if (c<node->c)
        {
            if (node->left==NULL)   
            {   
                node->left= new TernaryTreeNode<Index>();
                node->left->c=c;
             //   std::cerr<<"creating left\n";
            }
            node=node->left;
            //std::cerr<<"moving left\n";
           // continue;
        } else
        if (c>node->c)
        {
            if (node->right==NULL) 
            {
                node->right= new TernaryTreeNode<Index>();
                node->right->c=c;
            }
            node=node->right;
            //std::cerr<<"moving right\n";
            //continue;
        }
        //if (depth>=strlen(str)) is_done=true;
        if ((depth>=strlen(str)-1)&&(node->c==c)) is_done=true;
    }
    if (!node->data) node->id=id_global++;
    node->data++;

    return node->id;
}

/*
template <typename T>
void increment(TernaryTreeNode<T> * node, const char * str)
{
  if (head==NULL)
    { 
        head= new TernaryTreeNode<T>();
        head->c=str[0];
    }
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
*/

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

Index get_id(const TernaryTreeNode<Index> * node, const char * str)
{
    unsigned int depth=0;
    //std::cerr<<"fetching id for "<<str<<"\n";
    bool is_done=false;
    while (!is_done)
    {
        char c=str[depth];
        if (c==node->c)
        {
            if (node->down==NULL) return 0;
            node=node->down;
            depth++;
        } else
        if (c<node->c)
        {
            if (node->left==NULL)  return 0;
            node=node->left;
        } else
        if (c>node->c)
        {
            if (node->right==NULL) return 0;
            node=node->right;
        }
        c=str[depth];
        //std::cerr<<"depth = "<<depth<<" node.c = "<<node->c<<"\n";
        if ((depth>=strlen(str)-1)&&(node->c==c)) is_done=true;
    }
    //std::cerr<<"found at depth "<<depth<<" id = "<<node->id-1<<"\n";
    return node->id;
}
template <typename T>
void dump_frequency(std::ostream &file, const TernaryTreeNode<T> * node,unsigned int depth)
{
    buffer[depth]=node->c;  
    if (node->data)
    file<<std::string(buffer,buffer+depth+1)<<"\t"<<node->data<<"\n";
    if (node->left!=NULL) dump_frequency<T>(file,node->left,depth);
    buffer[depth]=node->c;  
    if (node->down!=NULL) dump_frequency<T>(file,node->down,depth+1);
    buffer[depth]=node->c;  
    if (node->right!=NULL) dump_frequency<T>(file,node->right,depth);
    buffer[depth]=node->c;  
}

template <typename T>
void dump_ids(std::ostream &file, const TernaryTreeNode<T> * node,unsigned int depth)
{
    buffer[depth]=node->c;  
    if (node->data)
    file<<std::string(buffer,buffer+depth+1)<<"\t"<<node->id<<"\n";
    if (node->left!=NULL) dump_ids<T>(file,node->left,depth);
    buffer[depth]=node->c;  
    if (node->down!=NULL) dump_ids<T>(file,node->down,depth+1);
    buffer[depth]=node->c;  
    if (node->right!=NULL) dump_ids<T>(file,node->right,depth);
    buffer[depth]=node->c;  
}

