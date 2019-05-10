// VCL configuration
#include <vcl/config/global.h>

// Include the relevant parts from the library
#include <vcl/core/simd/vectorscalar.h>
#include <vcl/math/math.h>

// C++ standard library
#include <iostream>

int main()
{
	using Vcl::float4;
	using Vcl::float8;
	using Vcl::float16;

	using Vcl::Mathematics::equal;

	// Source data
	float4  vec1{ 0.0f, 6.10116f, 11.6117f, 11.8436f };
	float8  vec2{ 0.0f, 6.10116f, 11.6117f, 11.8436f,
				  0.0f, 6.10116f, 11.6117f, 11.8436f };
	float16 vec3{ 0.0f, 6.10116f, 11.6117f, 11.8436f,
				  0.0f, 6.10116f, 11.6117f, 11.8436f,
				  0.0f, 6.10116f, 11.6117f, 11.8436f,
				  0.0f, 6.10116f, 11.6117f, 11.8436f };

	// Compute 1 / sqrt(x)
	float4  res1 = sqrt(vec1);
	float8  res2 = sqrt(vec2);
	float16 res3 = sqrt(vec3);

	// Reference result
	float4  ref1{ 0.0f, 2.4700526f, 3.4075945f, 3.4414532f };
	float8  ref2{ 0.0f, 2.4700526f, 3.4075945f, 3.4414532f,
				  0.0f, 2.4700526f, 3.4075945f, 3.4414532f };
	float16 ref3{ 0.0f, 2.4700526f, 3.4075945f, 3.4414532f,
				  0.0f, 2.4700526f, 3.4075945f, 3.4414532f,
				  0.0f, 2.4700526f, 3.4075945f, 3.4414532f,
				  0.0f, 2.4700526f, 3.4075945f, 3.4414532f };

	std::cout << all(equal(ref1, res1, float4(1e-5f))) << std::endl;
	std::cout << all(equal(ref2, res2, float8(1e-5f))) << std::endl;
	std::cout << all(equal(ref3, res3, float16(1e-5f))) << std::endl;
    return 0;
}
