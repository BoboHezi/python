1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
Code panel - press c to focus line 1.
load(
  "@lunch//:env.bzl",
  "TARGET_PRODUCT",
  "TARGET_BUILD_VARIANT",
  "COMBINED_NINJA",
  "KATI_NINJA",
  "PACKAGE_NINJA",
  "SOONG_NINJA"
)
ninja_graph(
    name = "combined_graph",
    main = COMBINED_NINJA,
    # This assumes that --skip-make is *not* used, so the Kati and Package files exists.
    ninja_srcs = [
        KATI_NINJA,
        PACKAGE_NINJA,
        SOONG_NINJA,
    ],
    # TODO(b/171012031): Stop hardcoding "out/".
    output_root = "out",
    # These files are created externally of the Ninja action graph, for
    # example, when Kati parses the product configuration Make files to
    # create soong/soong.variables.
    #
    # Since these aren't created by actions in the ninja_graph .ninja
    # inputs, Bazel will fail with missing inputs while executing
    # ninja_build. output_root_inputs allowlists these files for Bazel to
    # symlink them into the execution root, treating them as source files
    # in the output directory (toplevel_output_directories).
    output_root_inputs = [
        "build_date.txt",
        "empty",
        "soong/build_number.txt",
        "soong/dexpreopt.config",
        "soong/soong.variables",
    ],
    output_root_input_dirs = [
        "bazel/output/execroot/sourceroot",
        "bazel/output/execroot/bazel_tools",
        ".module_paths",
        "soong/.bootstrap",
        "soong/.minibootstrap",
    ],
)
ninja_build(
    name = "%s-%s" % (TARGET_PRODUCT, TARGET_BUILD_VARIANT),
    ninja_graph = ":combined_graph",
    output_groups = {
        "droid": ["droid"],
        # TODO(b/160568333): Stop hardcoding output groups statically for Ninja targets.
        # libc is declared here to support CI builds running USE_BAZEL=1 USE_BAZEL_ANALYSIS=1 m libc
        "libc": ["libc"],
    },
)