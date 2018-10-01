<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{file}}</title>
    <style>
        table {background-color: lightsteelblue; width: 100%; border-radius: 0.3em; margin-bottom: 1em;}
        td {border-style: solid; border-color: transparent; border-radius: 0.3em; width: 50%; font-family: sans-serif;}
        td.red {background-color: pink; border-color: red; font-family: monospace}
        td.green {background-color: lightgreen; border-color: darkgreen; font-family: monospace}
    </style>
</head>
<body>
% for change in changes:
<table>
    <tr>
        <td colspan="2">{{change['path']}}</td>
    </tr>
    <tr>
        % if not change['right']:
        <td class="red" colspan="2">{{change['left']}}</td>
        % elif not change['left']:
        <td class="green" colspan="2">{{change['right']}}</td>
        % else:
        <td class="red">{{change['left']}}</td>
        <td class="green">{{change['right']}}</td>
        % end
    </tr>
</table>
% end
</body>
</html>