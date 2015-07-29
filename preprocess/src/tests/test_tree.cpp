#include <iostream>
#include <list>
#include <locale>
#include <codecvt>
#include "../ternary_tree.hpp"


//#define MAX_STR_SIZE 100

//std::list<std::string> lst_test = {"apple","banana","kiwi","potato","tomato","pear","orange"};
//std::list<std::string> lst_test = {"ca","ac","ab","az","a","aaa"};
//std::list<std::string> lst_test = {"k","b","a","ba","c","z"};
//std::list<std::string> lst_test = {"c","ba","ba","a","a","xa","xa","z","z"};
std::list<std::wstring> lst_test = {L"c",L"b",L"a",L"b"};
//std::list<std::wstring> lst_test = {L"c"};
//std::list<std::string> lst_test = {"c","a","a"};

int main()
{
	std::cout<<"testing add\n";
	TernaryTree tree;
	for (std::wstring t: lst_test)
	{
		std::cerr<<"adding "<<wstring_to_utf8(t)<<"\n";
		tree.set_id_and_increment(t.c_str());
	}

	for (std::wstring t: lst_test)
	{
		std::cerr<<"id of "<<wstring_to_utf8(t)<<"\t is "<<tree.get_id(t.c_str())<<"\n";
	}


	std::wstring str=L"nonexisant";
	Index id = tree.get_id(str.c_str());
	std::cout<<"\nnonexistant id = " <<id<<"\n";
	size_t cnt_nodes=tree.count_nodes();
	std::cerr<<"\nnode count = "<<cnt_nodes<<"\twill take "<<cnt_nodes*sizeof(TernaryTreeNode<Index>)<<"b\n";
	tree.dump_ids("_ids_oroginal");
	tree.dump_frequency("_frequencies");
	tree.dump_dot("original.gv");
	trim(&(tree.tree),0,0);
	tree.reassign_ids();
	tree.dump_ids("_ids_reduced");
	tree.dump_dot("reduced.gv");

	str=L"nonexisant";
	id = tree.get_id(str.c_str());
	std::cout<<"\nnonexistant id after reduce = " <<id<<"\n";

}