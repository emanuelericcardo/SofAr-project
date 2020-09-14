% Function that computes the matrices for the joint limits (position &
% velocities) task.
% INPUTS: TODO
% OUTPUTS: TODO


function [J,A,rdot] = joint_constr(q,qdot,qmin,qmax,qdotmax,q_margin,qdot_margin,T)

    NJOINTS = length(q);
    
    rdot = zeros(NJOINTS,1); % task vector
    A = zeros(NJOINTS,NJOINTS); % activation matrix
    J = eye(NJOINTS); % Jacobian matrix
    
    qdotmin = -qdotmax;
    persistent k; % position correction poles
    persistent kv; % velocity correction poles
    
    if isempty(k) % first run
        k = zeros(NJOINTS,1);
        kv = zeros(NJOINTS,1);
    end
    
    % Function to evaluate qdot respectively in the case joint limit task
    % and joint velocity limit task is activated.
    fq = @(x,k,xstar,T) (k * (-x + xstar));
    fqdot = @(x,k,xstar,T) (k * (-x + xstar)*T + x);
    
    for ii = 1:NJOINTS
        % Compute activation matrix.
        A(ii,ii) = cosinoidal_sigmoid(q(ii),qmin(ii),qmax(ii),q_margin);
        
        % Compute task vector.
        [rdot(ii),k(ii),angleok] = compute_rdot(q(ii),qmin(ii),qmax(ii),q_margin,k(ii),0,fq,true);

        if angleok
            
            % Compute activation matrix.
            A(ii,ii) = cosinoidal_sigmoid(qdot(ii),qdotmin(ii),qdotmax(ii),qdot_margin);
            
            % Compute task vector.
            [rdot(ii),kv(ii),~] = compute_rdot(qdot(ii),qdotmin(ii),qdotmax(ii),qdot_margin,kv(ii),T,fqdot,false);
        end
    end
end



% Put desc here
% INPUT: TODO
% OUTPUT: TODO
function g = cosinoidal_sigmoid(x,xmin,xmax,x_margin)
    if x < xmin || x > xmax % x beyond semihard limits
        g = 1; % task fully activated
    elseif xmin >= xmin && x < xmin + x_margin % x getting too low
        g = 0.5 * (cos((x - xmin) * pi/x_margin) + 1); % g between 0 and 1
    elseif x <= xmax && x > xmax - x_margin % x getting too high
        g = 0.5 * (cos((x - xmax) * pi/x_margin) + 1); % g between 0 and 1
    else, g = 0; % x safe enough => task inactive
    end
end

% Put desc here
% INPUT: TODO
% OUTPUT: TODO
function [rdot,k,angleok] = compute_rdot(x,xmin,xmax,x_margin,k,T,f,is_joint)
    angleok = 0;
    if is_joint, corrpole = evalin('base','params.corrpole_joint');
    else, corrpole = evalin('base','params.corrpole_vel');
    end
    
    if x > xmax - x_margin % x too high
        if k == 0,k = corrpole;end
        xstar = xmax - x_margin;
        rdot = f(x,k,xstar,T);
    elseif x < xmin + x_margin % x too low
        if k == 0, k = corrpole;end
        xstar = xmin + x_margin;
        rdot = f(x,k,xstar,T);
    else, rdot = 0; k = 0; angleok = 1; % no correction was necessary
    end
end



% Author: Luca Tarasi.