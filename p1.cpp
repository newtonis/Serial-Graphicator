#include <bits/stdc++.h>
using namespace std;


#define rep(i,N) for(int i=0;i<(N);i++)
typedef long long ll;

const ll mod=100;
ll powmod(ll a,ll b) {ll res=1;a%=mod;for(;b;b>>=1){if(b&1)res=res*a%mod;a=a*a%mod;}return res;}


int main(){
	#ifndef ONLINE_JUDGE
	freopen("input.in","r",stdin);
	freopen("output.out","w+",stdout);
	#endif

	ll N; cin>>N;
	cout << powmod(5,N) << '\n';
}

