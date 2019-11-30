#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<time.h>
#include<string.h>
#include<utility>
#include<algorithm>
#include<set>
#include<math.h>
#include<stdlib.h>
#include<iostream>
#define X first
#define Y second
using namespace std;
const int MAXN = 300110;
const int MAXM = 900110;
const long double PI = 3.1415926535898;
const long double EPS = 1e-9;
typedef pair<long double, long double> Tpoint;
Tpoint a[MAXM][3];
int n;
pair<int, int> b[MAXM];
int f[MAXN], d[MAXN];
long double tmp;

struct Tnode
{
	long double p, v;
	int t, pos;
	inline bool operator==(const Tnode& x)
	{
		return (x.t == t) && (x.pos == pos);
	}
	inline long double value()
	{
		return (p + v * tmp);
	}
};

inline bool operator < (const Tnode& y, const Tnode& x)
{
	return (y.p + y.v * tmp < x.p + x.v * tmp - EPS) || (((fabs(y.p + y.v * tmp - x.p - x.v * tmp) < EPS) && (y.t < x.t)));
}

inline bool equal(long double x, long double y)
{
	return fabs(x - y) < EPS;

}

int cmp(const void* a, const void* b)
{
	return (*(long double*)a > * (long double*)b ? 1 : -1);
}

inline bool cmp2(const pair<int, int>& x, const pair<int, int>& y)
{
	return a[x.X][x.Y].X < a[y.X][y.Y].X;
}

inline void rorate(Tpoint& a, long double alpha)
{
	long double x, y;
	x = a.X * cos(alpha) - a.Y * sin(alpha);
	y = a.X * sin(alpha) + a.Y * cos(alpha);
	a.X = x;
	a.Y = y;
}

int getf(int p)
{
	if (p == -1)
		return 1;
	else if (d[p] != -1)
		return d[p];
	else
		return d[p] = getf(f[p]) + 1;
}


void init()
{
	int i, j, k, l;
	int tx, ty;
	for (i = 0; i < n; ++i)
		for (j = 0; j < 3; ++j)
		{
			scanf("%d %d", &tx, &ty);
			a[i][j].X = tx;
			a[i][j].Y = ty;
		}
	long double alpha = rand() % 30000 / 30000.0 * PI;
	for (i = 0; i < n; ++i)
	{
		for (j = 0; j < 3; ++j)
			rorate(a[i][j], alpha);
		qsort(a[i], 3, sizeof(long double) * 2, cmp);
		b[3 * i].X = b[3 * i + 1].X = b[3 * i + 2].X = i;
		b[3 * i].Y = 0;
		b[3 * i + 1].Y = 1;
		b[3 * i + 2].Y = 2;
	}
	sort(b, b + 3 * n, cmp2);
}

void solve()
{
	int i, j, k, l;
	Tnode t1, t2, t3;
	long double td;
	set<Tnode> t;
	set<Tnode> ::iterator i1, i2, i3, test1;
	t.clear();
	bool ok = 1;
	memset(f, 0xff, sizeof(f));
	for (i = 0; ok && (i < 3 * n); ++i)
	{
		j = b[i].X;
		k = b[i].Y;
		tmp = a[j][k].X;
		if (k == 0)
		{
			t1.v = (a[j][1].Y - a[j][0].Y) / (a[j][1].X - a[j][0].X);
			t1.p = a[j][0].Y - a[j][0].X * t1.v;
			t2.v = (a[j][2].Y - a[j][0].Y) / (a[j][2].X - a[j][0].X);
			t2.p = a[j][0].Y - a[j][0].X * t2.v;
			t1.pos = t2.pos = j;
			if (t1.v > t2.v)
			{
				t3 = t1;
				t1 = t2;
				t2 = t3;
			}
			t1.t = 0;
			t2.t = 1;
			i1 = t.lower_bound(t1);
			test1 = t.end();
			if ((i1 != t.end()))
			{
				t3 = (*i1);
				if (equal(t3.value(), t1.value())) {
					ok = false;
					break;
				}
			}
			t.insert(t1);
			t.insert(t2);
			i1 = t.find(t1);
			if (i1 == t.end())
			{
				ok = false;
				break;
			}
			if (i1 != t.begin())
			{
				i1--;
				if (i1->t == 1)
					f[j] = f[i1->pos];
				else
					f[j] = i1->pos;
			}
		}
		else if (k == 1)
		{
			//判断第二点与第一点属于第几条边
			if (((a[j][1].X - a[j][0].X) * (a[j][2].Y - a[j][0].Y) - (a[j][2].X - a[j][0].X) * (a[j][1].Y - a[j][0].Y)) > 0)
			{
				l = 0;
			}
			else
			{
				l = 1;
			}
			t1.v = (a[j][1].Y - a[j][0].Y) / (a[j][1].X - a[j][0].X);
			t1.p = a[j][0].Y - a[j][0].X * t1.v;
			t1.pos = j; //pos记录第几个三角形
			t1.t = l;
			td = t1.value();
			i1 = t.find(t1);
			if (i1 == t.end())
			{
				ok = false;
				break;
			}
			if (i1 != t.begin())
			{
				i1--;
				t3 = (*i1);
				if (td <= t3.value() + EPS)
				{
					ok = false;
					break;
				}
				i1++;
			}
			i1++;
			if (i1 != t.end())
			{
				t3 = (*i1);
				if (td >= t3.value() - EPS)
				{
					ok = false;
					break;
				}
			}
			t.erase(t1);
			t1.v = (a[j][2].Y - a[j][1].Y) / (a[j][2].X - a[j][1].X);
			t1.p = a[j][1].Y - a[j][1].X * t1.v;
			t.insert(t1);
		}
		else
		{
			if (((a[j][1].X - a[j][0].X) * (a[j][2].Y - a[j][0].Y) - (a[j][2].X - a[j][0].X) * (a[j][1].Y - a[j][0].Y)) <= 0)
			{
				t1.v = (a[j][2].Y - a[j][0].Y) / (a[j][2].X - a[j][0].X);
				t1.p = a[j][0].Y - a[j][0].X * t1.v;
			}
			else
			{
				t1.v = (a[j][2].Y - a[j][1].Y) / (a[j][2].X - a[j][1].X);
				t1.p = a[j][1].Y - a[j][1].X * t1.v;
			}
			t1.pos = j;
			t1.t = 0;
			i2 = t.find(t1);
			i1 = i2++;
			if ((i1 == t.end()) || (i2 == t.end()) || (i2->pos != j) || (i2->t != 1))//当发现边不对时出错
			{
				ok = false;
				break;
			}
			td = t1.value();
			i3 = i2++;
			t.erase(i3);
			if (i2 != t.end())
			{
				t3 = (*i2);
				if (t3.value() <= EPS + td)
				{
					ok = false;
					break;
				}
			}
			i3 = i1--;
			if (i3 != t.begin())
			{
				t3 = (*i1);
				if (t3.value() >= td - EPS)
				{
					ok = false;
					break;
				}
			}
			t.erase(i3);
		}
	}
	if (!ok)
	{
		printf("ERROR\n");
		return;
	}
	int ans = 1;
	memset(d, 0xff, sizeof(d));
	for (i = 0; i < n; ++i)
		ans = max(ans, getf(i));
	printf("%d shades\n", ans);
}

int main()
{
	srand(time(NULL));
	int CASE = 0;
	while ((scanf("%d", &n) != EOF) && (n != -1))
	{
		init();
		printf("Case %d: ", ++CASE);
		solve();
	}
	return 0;
}
