#define MAX_STR_SIZE  1500
#include <cstring>

char  buffer[MAX_STR_SIZE];
//unsigned long long cnt_words;
//std::ofstream file;

typedef size_t Index;
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

class TernaryTree
{
private:
public:
    TernaryTreeNode<Index> * tree;
    TernaryTree():tree(NULL)
    {
        tree = new TernaryTreeNode<unsigned long>();
        tree->c='m';
    }
//Index get_value(const TernaryTreeNode<Index> * node, const char * str) ;
    Index get_id(const char * str);
    Index set_id_and_increment(const char * str);
    void dump_frequency(const std::string & name_file) const;
    void dump_ids(const std::string & name_file) const;
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
    
Index TernaryTree::set_id_and_increment(const char * str)
{
    auto node=tree;
/*  if (node==NULL)
    { 
        head= new TernaryTreeNode<T>();
        head->c=str[0];
    }*/ 
    //TernaryTreeNode<T> * node = head;
    unsigned int depth=0;
    bool is_done=false;
    while (!is_done)
    {
        if (depth>=MAX_STR_SIZE) {std::cerr<<"string too long in tree, aborting \n"; return -1;}
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

//template <typename T>
/*
Index TernaryTree::get_value(const TernaryTreeNode<Index> * node, const char * str) 
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
*/

Index TernaryTree::get_id(const char * str)
{
    auto node=tree;
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

class Action
{
public:
    virtual void operator()(const TernaryTreeNode<Index>* node,unsigned int depth)=0;
};

class ActionFile: public Action
{
protected:
    std::ofstream file;
public:
    ActionFile(std::string name_file)
    {
        file.open (name_file);    
        if(!file)  throw  std::runtime_error("can not open output file "+name_file+" , check the path");
    }
    virtual ~ActionFile()
    {
        file.close();
    }
};

class ActionFileWriteFrequency: public ActionFile
{
public:
    ActionFileWriteFrequency(std::string name_file):ActionFile(name_file){}
    void operator()(const TernaryTreeNode<Index>* node,unsigned int depth)
    {
        file<<std::string(buffer,buffer+depth+1)<<"\t"<<node->data<<"\n";
    }
};

class ActionFileWriteId: public ActionFile
{
public:
    ActionFileWriteId(std::string name_file):ActionFile(name_file){}
    void operator()(const TernaryTreeNode<Index>* node,unsigned int depth)
    {
        file<<std::string(buffer,buffer+depth+1)<<"\t"<<node->id<<"\n";
    }
};

void visit_recursively(const TernaryTreeNode<Index> * node,unsigned int depth, Action & action)
{
    buffer[depth]=node->c;  
    if (node->data)
        action(node,depth);
    if (node->left!=NULL) visit_recursively(node->left,depth,action);
    buffer[depth]=node->c;  
    if (node->down!=NULL) visit_recursively(node->down,depth+1,action);
    buffer[depth]=node->c;  
    if (node->right!=NULL) visit_recursively(node->right,depth,action);
    buffer[depth]=node->c;  
}


void TernaryTree::dump_frequency(const std::string & name_file) const
{
    ActionFileWriteFrequency a(name_file);
    visit_recursively(tree,0,a);
}

void TernaryTree::dump_ids(const std::string & name_file) const
{
    ActionFileWriteId a(name_file);
    visit_recursively(tree,0,a);
}

