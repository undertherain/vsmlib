#include <cstring>
#include <fstream>
#include <stdexcept>
#include <codecvt>
#include <locale>
#include "ternary_tree.hpp"

//#define MAX_STR_SIZE  1500
wchar_t  buffer[MAX_STR_SIZE];


Index TernaryTree::set_id_and_increment(const wchar_t * str)
{
    if (tree==NULL)
    { 
        //std::cerr<<"creating new head\n";
        tree = new TernaryTreeNode<Index>();
        tree->c=str[0];
        //tree->data=id_global++;
    } 
    auto node=tree;
    unsigned int depth=0;
    bool is_done=false;
    if ((wcslen(str)==1)&&(node->c==str[0])) is_done=true;
    while (!is_done)
    {
        if (depth>=MAX_STR_SIZE) {std::cerr<<"string too long in tree, aborting \n"; return -1;}
        wchar_t c=str[depth];
//        std::cerr<<"depth = "<<depth<<"\tnode.c = "<<node->c<<"\tc = "<<c<<"\n";
        if (c==node->c)
        {
            if (node->down==NULL) 
            {
                node->down= new TernaryTreeNode<Index>();
                node->down->c=str[depth+1];     
//                std::cerr<<"creating down\n";
            }
            node=node->down;
//            std::cerr<<"moving down\n";
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
//                std::cerr<<"creating left\n";
            }
            node=node->left;
//            std::cerr<<"moving left\n";
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
//            std::cerr<<"moving right\n";
            //continue;
        }
        //if (depth>=strlen(str)) is_done=true;
        if ((depth>=wcslen(str)-1)&&(node->c==c)) is_done=true;
    }
    if (!node->data) node->id=id_global++;
    node->data++;
    return node->id;
}

TernaryTreeNode<Index> * TernaryTree::get_node(const wchar_t * str)
{
    auto node=tree;
    unsigned int depth=0;
    //std::cerr<<"fetching id for "<<str<<"\n";
    bool is_done=false;
    while (!is_done)
    {
        wchar_t c=str[depth];
        if (c==node->c)
        {
            if (node->down==NULL) return NULL;
            node=node->down;
            depth++;
        } else
        if (c<node->c)
        {
            if (node->left==NULL)  return NULL;
            node=node->left;
        } else
        if (c>node->c)
        {
            if (node->right==NULL) return NULL;
            node=node->right;
        }
        c=str[depth];
        //std::cerr<<"depth = "<<depth<<" node.c = "<<node->c<<"\n";
        if ((depth>=wcslen(str)-1)&&(node->c==c)) is_done=true;
    }
    return node;
}


Index TernaryTree::get_id(const wchar_t * str)
{
    auto node=tree;
    if (node==NULL) return -1;
    unsigned int depth=0;
    bool is_done=false;
    while (!is_done)
    {
        wchar_t c=str[depth];
        if (c==node->c)
        {
            if (depth>=wcslen(str)-1) return node->id;
            if (node->down==NULL) return -1;
            node=node->down;
            depth++;
        } else
        if (c<node->c)
        {
            if (node->left==NULL)  return -1;
            node=node->left;
        } else
        if (c>node->c)
        {
            if (node->right==NULL) return -1;
            node=node->right;
        }
        c=str[depth];
        //std::cerr<<"depth = "<<depth<<" node.c = "<<node->c<<"\n";
        if ((depth>=wcslen(str)-1)&&(node->c==c)) is_done=true;
    }
    //std::cerr<<"found at depth "<<depth<<" id = "<<node->id-1<<"\n";
    return node->id;
}
/*

class Action {
public:
    virtual void operator()(TernaryTreeNode<Index>* node,unsigned int depth)=0;
};

class ActionReassignIds: public Action {
public:
    uint64_t current_id;
    ActionReassignIds():current_id(0){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
        if (node->data>0) node->id=current_id++;
    }
};

class ActionReassignIdsFreq: public Action {
public:
    std::vector<Index> const & lst_new_ids;
    ActionReassignIdsFreq(std::vector<Index> const & _lst_new_ids):lst_new_ids(_lst_new_ids){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
        if (node->data>0) 
            if (node->id>=0) 
        {
           //   std::cerr<<"replaceing "<<node->id<<" with "<<lst_new_ids[node->id]<<"\n";
            node->id=lst_new_ids[node->id];
        }
    }
};
*/

ActionFile::ActionFile(std::string name_file)
    {
        file.open (name_file);    
        if(!file)  throw  std::runtime_error("can not open output file "+name_file+" , check the path");
    }
ActionFile::~ActionFile()
    {
        file.close();
    }

void ActionFileWriteFrequency::operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
    if (node->data)
        file<<wstring_to_utf8(std::wstring(buffer,buffer+depth+1))<<"\t"<<node->data<<"\n";
    }


void ActionFileWriteId::operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
    if (node->data)
        file<<wstring_to_utf8(std::wstring(buffer,buffer+depth+1))<<"\t"<<node->id<<"\n";
    }

void ActionCountNodes::operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
        cnt++;
    }


ActionFileWriteDot::ActionFileWriteDot(std::string name_file):ActionFile(name_file)
    {
        file<<"digraph tree {\n";
    }
ActionFileWriteDot::~ActionFileWriteDot()
    {
        file<<"}\n";
    }
    
void ActionFileWriteDot::operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
    std::wstring label(buffer,buffer+depth+1);
    file<<wstring_to_utf8(label)<<" [label="<<node->c<<"];\n";
    if (node->left!=NULL)
    {
        std::wstring label2=label;
        label2[label2.length()-1]=node->left->c;
        file<<wstring_to_utf8(label)<<"\t->\t"<<wstring_to_utf8(label2)<<"  [color=blue];\n";
    }
    if (node->down!=NULL)
    {
        std::wstring label2=label;
        label2=label2+node->down->c;
        file<<wstring_to_utf8(label)<<"\t->\t"<<wstring_to_utf8(label2)<<" [style=dotted];\n";
    }
    if (node->right!=NULL)
    {
        std::wstring label2=label;
        label2[label2.length()-1]=node->right->c;
        file<<wstring_to_utf8(label)<<"\t->\t"<<wstring_to_utf8(label2)<<"[color=red] ;\n";
    }
        
    }


void visit_recursively(TernaryTreeNode<Index> * node,unsigned int depth, Action & action)
{
    if (node==NULL) return;
    buffer[depth]=node->c;  
    if (node->left!=NULL) visit_recursively(node->left,depth,action);
    buffer[depth]=node->c;  
    buffer[depth+1]=0;  

    action(node,depth);

    if (node->down!=NULL) visit_recursively(node->down,depth+1,action);
    buffer[depth]=node->c;  
    if (node->right!=NULL) visit_recursively(node->right,depth,action);
    buffer[depth]=node->c;  
}

void ActionPopulateFrequency::operator()(TernaryTreeNode<Index>* node,unsigned int depth)
{
    if (node->id>=0)
    lst_frequency[node->id]=node->data;
}


bool trim(TernaryTreeNode<Index> * * pnode, int64_t threshold, unsigned int depth)
{
    auto node = * pnode;
    if (node==NULL) return true;

    buffer[depth]=node->c;  

    int cnt_kids=3;
    if (trim(&(node->left),threshold,depth))
    {
        cnt_kids--;
    }
    if (trim(&(node->down),threshold,depth+1))
    {
        cnt_kids--;
    }

    if (trim(&(node->right),threshold,depth))
    {
        cnt_kids--;
    }

    if (node->data<threshold)
    {
        if (cnt_kids==0)
        {
            delete *pnode;
            *pnode=NULL;
            return true;
        }
        else
        {
            node->id=-1;
            node->data=0;
        }
    }
    return false;
}



void TernaryTree::populate_frequency(std::vector<Index> & lst_frequency ) const
{
    ActionPopulateFrequency a(lst_frequency);
    visit_recursively(tree,0,a);
}

void TernaryTree::dump_frequency(const std::string & name_file) const
{
    ActionFileWriteFrequency a(name_file);
    visit_recursively(tree,0,a);
}

void TernaryTree::dump_dot(const std::string & name_file) const
{
    ActionFileWriteDot a(name_file);
    visit_recursively(tree,0,a);
}

void TernaryTree::dump_ids(const std::string & name_file) const
{
    ActionFileWriteId a(name_file);
    visit_recursively(tree,0,a);
}

void TernaryTree::reassign_ids()
{
    ActionReassignIds a;
    visit_recursively(tree,0,a);
    id_global=a.current_id;
}

void TernaryTree::reassign_ids_new(std::vector<Index> const  & lst_new_ids)
{
    ActionReassignIdsFreq a(lst_new_ids);
    visit_recursively(tree,0,a);
}

size_t TernaryTree::count_nodes() const
{
    ActionCountNodes a;
    visit_recursively(tree,0,a);
    return a.cnt;
}
